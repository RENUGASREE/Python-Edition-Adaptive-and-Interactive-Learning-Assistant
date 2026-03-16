import { Layout } from "@/components/Layout";
import { useAuth } from "@/hooks/use-auth";
import { useUserProgress } from "@/hooks/use-progress";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { User, Mail, Calendar, Edit3, Save, X, Camera, Award, Target } from "lucide-react";
import { useState, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";

interface UpdateProfileData {
  firstName: string;
  lastName: string;
  email: string;
}

async function updateProfile(data: UpdateProfileData): Promise<any> {
  const accessToken = getAccessToken();

  const response = await fetch(apiUrl("/auth/user/update"), {
    method: "POST",  // Using POST to avoid CSRF issues
    headers: {
      "Content-Type": "application/json",
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
    credentials: "include",
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to update profile" }));
    throw new Error(error.message || "Failed to update profile");
  }

  return response.json();
}

async function uploadProfileImage(file: File): Promise<{ profileImageUrl: string }> {
  const accessToken = getAccessToken();

  const formData = new FormData();
  formData.append("profile_image", file);

  const response = await fetch(apiUrl("/auth/user/avatar"), {
    method: "POST",
    headers: {
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
    credentials: "include",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: "Failed to upload image" }));
    throw new Error(error.message || "Failed to upload image");
  }

  return response.json();
}

export default function Profile() {
  const { user } = useAuth();
  const { data: progress } = useUserProgress();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    firstName: user?.firstName || "",
    lastName: user?.lastName || "",
    email: user?.email || "",
  });

  const updateProfileMutation = useMutation({
    mutationFn: updateProfile,
    onSuccess: (data) => {
      queryClient.setQueryData(["/api/auth/user"], data);
      toast({
        title: "Success",
        description: "Profile updated successfully",
      });
      setIsEditing(false);
    },
    onError: (error: any) => {
      console.error("Profile update error:", error);
      toast({
        title: "Update failed",
        description: error.message || "Please check your input and try again.",
        variant: "destructive",
      });
    },
  });

  const uploadImageMutation = useMutation({
    mutationFn: uploadProfileImage,
    onSuccess: (data) => {
      queryClient.setQueryData(["/api/auth/user"], (old: any) => ({
        ...old,
        profileImageUrl: data.profileImageUrl,
      }));
      toast({
        title: "Success",
        description: "Profile image updated successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleInputChange = (field: keyof typeof formData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    updateProfileMutation.mutate(formData);
  };

  const handleCancel = () => {
    setFormData({
      firstName: user?.firstName || "",
      lastName: user?.lastName || "",
      email: user?.email || "",
    });
    setIsEditing(false);
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        toast({
          title: "Error",
          description: "Image size must be less than 5MB",
          variant: "destructive",
        });
        return;
      }
      uploadImageMutation.mutate(file);
    }
  };

  const getInitials = () => {
    const first = user?.firstName?.[0] || "";
    const last = user?.lastName?.[0] || "";
    return (first + last).toUpperCase() || "U";
  };

  const memberSinceRaw = (user as any)?.createdAt || (user as any)?.dateJoined;
  const memberSince = memberSinceRaw 
    ? new Date(memberSinceRaw as unknown as string).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    : "Not available";
  const isDirty = (
    formData.firstName !== (user?.firstName || "") ||
    formData.lastName !== (user?.lastName || "") ||
    formData.email !== (user?.email || "")
  );

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-display font-bold">Profile</h1>
          {!isEditing && (
            <Button onClick={() => setIsEditing(true)} variant="outline">
              <Edit3 className="w-4 h-4 mr-2" />
              Edit Profile
            </Button>
          )}
        </div>

        {/* Profile Overview Card */}
        <Card className="border border-border">
          <CardHeader>
            <CardTitle>Profile Information</CardTitle>
            <CardDescription>Manage your personal information and preferences</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Avatar Section */}
            <div className="flex items-center gap-6">
              <div className="relative">
                <Avatar className="h-20 w-20">
                  {user?.profileImageUrl ? (
                    <AvatarImage src={user.profileImageUrl} alt="Profile" />
                  ) : (
                    <AvatarFallback className="text-xl">
                      {getInitials()}
                    </AvatarFallback>
                  )}
                </Avatar>
                <Button
                  size="icon"
                  variant="secondary"
                  className="absolute -bottom-2 -right-2 rounded-full w-8 h-8"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploadImageMutation.isPending}
                >
                  <Camera className="w-4 h-4" />
                </Button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
              </div>
              <div>
                <h3 className="text-lg font-semibold">
                  {user?.firstName || user?.lastName 
                    ? `${user.firstName || ''} ${user.lastName || ''}`.trim() 
                    : user?.username || "User"}
                </h3>
                <p className="text-sm text-muted-foreground">{user?.email}</p>
                <div className="flex items-center gap-2 mt-2">
                  <Badge variant="secondary">Member</Badge>
                  <Badge variant="outline">Python Learner</Badge>
                </div>
              </div>
            </div>

            <Separator />

            {/* Profile Form */}
            <div className="grid gap-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName">First Name</Label>
                  {isEditing ? (
                    <Input
                      id="firstName"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange("firstName", e.target.value)}
                      placeholder="Enter your first name"
                    />
                  ) : (
                    <div className="p-3 bg-muted rounded-lg">
                      {user?.firstName || "Not provided"}
                    </div>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Last Name</Label>
                  {isEditing ? (
                    <Input
                      id="lastName"
                      value={formData.lastName}
                      onChange={(e) => handleInputChange("lastName", e.target.value)}
                      placeholder="Enter your last name"
                    />
                  ) : (
                    <div className="p-3 bg-muted rounded-lg">
                      {user?.lastName || "Not provided"}
                    </div>
                  )}
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                {isEditing ? (
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    placeholder="Enter your email"
                  />
                ) : (
                  <div className="p-3 bg-muted rounded-lg flex items-center gap-2">
                    <Mail className="w-4 h-4 text-muted-foreground" />
                    {user?.email || "Not provided"}
                  </div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            {isEditing && (
              <div className="flex gap-3">
                <Button 
                  onClick={handleSave} 
                  disabled={updateProfileMutation.isPending || !isDirty}
                >
                  {updateProfileMutation.isPending ? (
                    <>
                      <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4 mr-2" />
                      Save Changes
                    </>
                  )}
                </Button>
                <Button onClick={handleCancel} variant="outline">
                  <X className="w-4 h-4 mr-2" />
                  Cancel
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Additional Info Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                Account Information
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="text-sm text-muted-foreground">Member Since</div>
                <div className="font-medium">{memberSince}</div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Account Status</div>
                <Badge variant="default" className="mt-1">Active</Badge>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5" />
                Learning Progress
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="text-sm text-muted-foreground">Completed Lessons</div>
                <div className="font-medium">{progress?.filter(p => p.completed).length || 0} lessons</div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Total Progress</div>
                <div className="font-medium flex items-center gap-2">
                  <Award className="w-4 h-4" />
                  {progress?.length || 0} topics started
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
}

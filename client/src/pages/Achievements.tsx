import { Trophy, Star, Target, Award, Zap, Crown } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/hooks/use-auth";
import { Layout } from "@/components/Layout";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";

const iconMap: Record<string, any> = {
  Star,
  Target,
  Zap,
  Award,
  Crown
};

export default function Achievements() {
  const { user } = useAuth();
  const [selectedCategory, setSelectedCategory] = useState("All");
  const { data: summary } = useQuery({
    queryKey: ["/api/gamification/summary"],
    queryFn: async () => {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/gamification/summary"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return null;
      if (!res.ok) throw new Error("Failed to fetch gamification summary");
      return res.json();
    },
  });

  const achievements = user?.achievements?.map(a => ({
    ...a,
    icon: iconMap[a.icon] || Star
  })) || [];
  
  const totalPoints = summary?.xp ?? achievements.filter(a => a.unlocked).reduce((sum, a) => sum + a.points, 0);
  const unlockedCount = achievements.filter(a => a.unlocked).length;
  const totalAchievements = achievements.length;
  const currentStreak = summary?.streak?.current ?? user?.stats?.streak ?? 0;

  const categories = ["All", "Beginner", "Challenges", "Consistency", "Progress", "Mastery"];

  const filteredAchievements = selectedCategory === "All" 
    ? achievements 
    : achievements.filter(a => a.category === selectedCategory);

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Achievements</h1>
            <p className="text-muted-foreground">
              Track your progress and unlock rewards as you learn
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-yellow-500" />
            <span className="text-2xl font-bold">{totalPoints}</span>
            <span className="text-muted-foreground">points</span>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Unlocked</CardTitle>
              <Trophy className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{unlockedCount}/{totalAchievements}</div>
              <Progress value={totalAchievements ? (unlockedCount / totalAchievements) * 100 : 0} className="mt-2" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total Points</CardTitle>
              <Star className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalPoints}</div>
              <p className="text-xs text-muted-foreground">
                Earn points by completing achievements
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
              <Zap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{currentStreak}</div>
              <p className="text-xs text-muted-foreground">
                Keep it up! Learning days in a row
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Categories */}
        <div className="flex gap-2 overflow-x-auto pb-2">
          {categories.map((category) => (
            <Badge
              key={category}
              variant={category === selectedCategory ? "default" : "secondary"}
              className="cursor-pointer hover:bg-primary/90"
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </Badge>
          ))}
        </div>

        {/* Achievements Grid */}
        <div className="grid gap-4 md:grid-cols-2">
          {filteredAchievements.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="p-6 text-sm text-muted-foreground">
                No achievements yet. Complete lessons to unlock your first badge.
              </CardContent>
            </Card>
          ) : (
            filteredAchievements.map((achievement) => (
              <Card key={achievement.id} className={!achievement.unlocked ? "opacity-60" : ""}>
                <CardContent className="p-6">
                  <div className="flex items-start gap-4">
                    <div className={`p-2 rounded-lg ${achievement.unlocked ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"}`}>
                      <achievement.icon className="w-6 h-6" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="font-semibold">{achievement.title}</h3>
                        <Badge variant={achievement.unlocked ? "default" : "outline"}>
                          {achievement.points} pts
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-3">
                        {achievement.description}
                      </p>
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs text-muted-foreground">
                          <span>Progress</span>
                          <span>{achievement.progress}/{achievement.maxProgress}</span>
                        </div>
                        <Progress value={(achievement.progress / achievement.maxProgress) * 100} />
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </Layout>
  );
}

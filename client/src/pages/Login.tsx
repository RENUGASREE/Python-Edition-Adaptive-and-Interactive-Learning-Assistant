import { Navbar } from "@/components/Navbar";
import { useAuth } from "@/hooks/use-auth";
import { Eye, EyeOff, Loader2, LogIn, UserPlus } from "lucide-react";
import { useEffect, useState } from "react";
import { useLocation } from "wouter";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useQueryClient } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";

export default function Login() {
  const { user, isLoading } = useAuth();
  const queryClient = useQueryClient();
  const [, setLocation] = useLocation();
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [mode, setMode] = useState<"login" | "register">("login");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState<string | null>(null);

  function isStrongPassword(pw: string) {
    const minLen = pw.length >= 8;
    const hasUpper = /[A-Z]/.test(pw);
    const hasLower = /[a-z]/.test(pw);
    const hasDigit = /\d/.test(pw);
    const hasSpecial = /[!@#$%^&*()_\-+=\[\]{}|;:,.<>/?`~]/.test(pw);
    return minLen && hasUpper && hasLower && hasDigit && hasSpecial;
  }

  useEffect(() => {
    if (user) {
      window.location.href = "/dashboard";
    }
  }, [user, setLocation]);

  const handleSubmit = async () => {
    setIsLoggingIn(true);
    setError(null);
    try {
      if (mode === "register" && password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }
      const endpoint =
        mode === "login"
          ? apiUrl("/auth/login")
          : apiUrl("/auth/register");
      const body =
        mode === "login"
          ? { identifier, password }
          : { email: identifier, password, firstName: firstName || undefined, lastName: lastName || undefined };
      
      if (mode === "register" && !isStrongPassword(password)) {
        setError("Use a strong password: min 8 chars with uppercase, lowercase, number, and special character.");
        return;
      }

      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.message || "Invalid credentials");
      }
      
      // Store JWT tokens if login/register was successful
      const data = await res.json();
      if (data.access && data.refresh) {
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        
        // Force refetch user data to update UI immediately
        await queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
      }
      
      setLocation("/dashboard");
    } catch (e: any) {
      setError(e.message || "Failed");
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    handleSubmit();
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="max-w-md mx-auto py-16 px-4">
        <Card className="bg-card/60 border-border/60">
          <CardHeader>
            <CardTitle className="font-display">
              {mode === "login" ? "Sign in" : "Create account"}
            </CardTitle>
            <CardDescription>
              {mode === "login" ? "Enter your credentials." : "Register to start learning."}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={handleFormSubmit}>
              {mode === "register" && (
                <>
                  <input
                    type="text"
                    placeholder="First name"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="w-full px-4 py-3 bg-muted/50 border border-transparent focus:border-primary rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
                  />
                  <input
                    type="text"
                    placeholder="Last name"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="w-full px-4 py-3 bg-muted/50 border border-transparent focus:border-primary rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
                  />
                </>
              )}
              <input
                type="text"
                placeholder={mode === "login" ? "Email or username" : "Email"}
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                className="w-full px-4 py-3 bg-muted/50 border border-transparent focus:border-primary rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
              />
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 pr-12 bg-muted/50 border border-transparent focus:border-primary rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {mode === "register" && (
                <div>
                  <input
                    type={showPassword ? "text" : "password"}
                    placeholder="Confirm password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-3 bg-muted/50 border border-transparent focus:border-primary rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20"
                  />
                </div>
              )}

              {error && <div className="text-sm text-destructive">{error}</div>}

              <Button
                type="submit"
                disabled={isLoading || isLoggingIn}
                className="w-full flex items-center justify-center gap-2"
              >
                {isLoggingIn ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : mode === "login" ? (
                  <LogIn className="w-4 h-4" />
                ) : (
                  <UserPlus className="w-4 h-4" />
                )}
                <span>{mode === "login" ? "Sign in" : "Create account"}</span>
              </Button>

              <div className="text-sm text-center pt-2">
                {mode === "login" ? (
                  <>
                    Don’t have an account?{" "}
                    <button
                      className="text-primary underline underline-offset-2"
                      onClick={() => setMode("register")}
                    >
                      Create one
                    </button>
                  </>
                ) : (
                  <>
                    Already have an account?{" "}
                    <button
                      className="text-primary underline underline-offset-2"
                      onClick={() => setMode("login")}
                    >
                      Sign in
                    </button>
                  </>
                )}
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

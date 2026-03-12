import { Link, useLocation } from "wouter";
import { Terminal, Menu, X, User } from "lucide-react";
import { useState } from "react";
import { useAuth } from "@/hooks/use-auth";
import { cn } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

export function Navbar() {
  const { user, logout, isLoggingOut } = useAuth();
  const [open, setOpen] = useState(false);
  const [, setLocation] = useLocation();
  const hasTakenQuiz = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);
  const navItems = user
    ? [
        { href: "/dashboard", label: "Dashboard" },
        { href: "/curriculum", label: "Curriculum" },
        { href: "/achievements", label: "Achievements" },
        { href: "/analytics", label: "Analytics" },
      ]
    : [
        { href: "/", label: "Home" },
        { href: "/auth", label: "Sign In" }, // Changed from /signin to /auth
      ];

  return (
    <nav className="border-b border-white/5 bg-[#0f1115]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2 font-display font-bold text-2xl text-primary">
          <Terminal className="w-7 h-7" />
          <span>PyLearn</span>
        </div>
        <div className="flex items-center gap-3">
          <button
            className="md:hidden p-2 text-muted-foreground hover:text-white"
            onClick={() => setOpen(!open)}
          >
            {open ? <X /> : <Menu />}
          </button>
          <div
            className={cn(
              "hidden md:flex items-center gap-4",
              open && "absolute top-16 left-0 right-0 bg-[#0f1115] p-4 border-b border-white/10 md:static md:p-0 md:border-0 md:bg-transparent md:flex"
            )}
          >
            {navItems.map((item) => {
              const locked = !!user && !hasTakenQuiz && item.href !== "/dashboard";
              if (locked) {
                return (
                  <button
                    key={item.href}
                    className="px-3 py-2 text-sm font-medium text-muted-foreground opacity-60"
                    onClick={() => {
                      try {
                        localStorage.setItem("quizGateMessage", "Please complete the placement quiz first.");
                      } catch {}
                      setLocation("/dashboard");
                    }}
                  >
                    {item.label}
                  </button>
                );
              }
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className="px-3 py-2 text-sm font-medium text-muted-foreground hover:text-white transition-colors"
                >
                  {item.label}
                </Link>
              );
            })}
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger className="outline-none">
                  <div className="flex items-center gap-2">
                    <Avatar className="h-8 w-8">
                      {user.profileImageUrl && (
                        <AvatarImage src={user.profileImageUrl} alt="Profile" />
                      )}
                      <AvatarFallback>
                        <User className="w-4 h-4 text-muted-foreground" />
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm text-white/80 max-w-[160px] truncate hidden md:block">
                      {user.firstName || "User"}
                    </span>
                  </div>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem asChild>
                    <Link href="/profile">Profile</Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/settings">Settings</Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href="/dashboard">Dashboard</Link>
                  </DropdownMenuItem>
                  {/* ... other items ... */}
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onClick={() => logout()}
                    className="text-destructive"
                  >
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <div className="flex items-center gap-4">
                <Link
                  href="/auth"
                  className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-white transition-colors"
                >
                  Log in
                </Link>
                <Link
                  href="/auth?mode=register"
                  className="px-4 py-2 text-sm font-bold bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-colors"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

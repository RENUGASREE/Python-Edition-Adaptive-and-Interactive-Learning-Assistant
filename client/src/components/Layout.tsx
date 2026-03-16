import { ReactNode } from "react";
import { Link, useLocation } from "wouter";
import { useAuth } from "@/hooks/use-auth";
import { 
  LayoutDashboard, 
  BookOpen, 
  Trophy, 
  LogOut, 
  Menu, 
  X,
  User,
  Terminal,
  BrainCircuit
} from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const [location, setLocation] = useLocation();
  const hasTakenQuiz = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);
  const [gateOpen, setGateOpen] = useState(false);

  const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/curriculum", label: "Curriculum", icon: BookOpen },
    { href: "/achievements", label: "Achievements", icon: Trophy },
    { href: "/analytics", label: "Analytics", icon: BrainCircuit },
    { href: "/challenges", label: "Challenges", icon: Terminal },
  ];

  return (
    <div className="min-h-screen bg-background flex flex-col md:flex-row">
      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between p-4 border-b border-border bg-card">
        <div className="flex items-center gap-2 font-display font-bold text-xl text-primary">
          <Terminal className="w-6 h-6" />
          <span>PyLearn</span>
        </div>
        <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="p-2 text-foreground">
          {isSidebarOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Sidebar */}
      <aside className={cn(
        "fixed md:sticky top-0 z-40 w-64 h-screen bg-card border-r border-border transition-transform duration-300 ease-in-out transform",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}>
        <div className="p-6 flex flex-col h-full">
          <div className="hidden md:flex items-center gap-3 font-display font-bold text-2xl text-primary mb-10">
            <div className="bg-primary/10 p-2 rounded-lg">
              <Terminal className="w-6 h-6" />
            </div>
            <span>PyLearn</span>
          </div>

          <nav className="flex-1 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location === item.href;
              const locked = !hasTakenQuiz && item.href !== "/dashboard";
              return (
                locked ? (
                  <div
                    key={item.href}
                    onClick={() => setGateOpen(true)}
                    className={cn(
                      "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 cursor-pointer group opacity-60",
                      isActive 
                        ? "bg-primary text-primary-foreground shadow-lg shadow-primary/25" 
                        : "text-muted-foreground hover:bg-muted"
                    )}
                  >
                    <Icon className={cn("w-5 h-5")} />
                    <span className="font-medium">{item.label}</span>
                  </div>
                ) : (
                  <Link key={item.href} href={item.href}>
                    <div className={cn(
                      "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 cursor-pointer group",
                      isActive 
                        ? "bg-primary text-primary-foreground shadow-lg shadow-primary/25" 
                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                    )}>
                      <Icon className={cn("w-5 h-5", isActive ? "text-primary-foreground" : "group-hover:text-primary")} />
                      <span className="font-medium">{item.label}</span>
                    </div>
                  </Link>
                )
              );
            })}
          </nav>

          <div className="border-t border-border pt-6 mt-6">
            <Link href="/profile" className="block">
              <div className="flex items-center gap-3 px-4 mb-4 hover:bg-muted rounded-lg p-2 transition-colors cursor-pointer">
                <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center overflow-hidden border-2 border-primary/20">
                  {user?.profileImageUrl ? (
                    <img src={user.profileImageUrl} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <User className="w-5 h-5 text-muted-foreground" />
                  )}
                </div>
                <div className="flex-1 overflow-hidden">
                  <p className="font-medium truncate text-sm">{user?.firstName || user?.username || 'User'}</p>
                  <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
                </div>
              </div>
            </Link>
            <button 
              onClick={() => logout()}
              className="w-full flex items-center gap-3 px-4 py-2 text-sm text-muted-foreground hover:text-destructive transition-colors rounded-lg hover:bg-destructive/10"
            >
              <LogOut className="w-4 h-4" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto h-[calc(100vh-64px)] md:h-screen p-4 md:p-8">
        <div className="max-w-6xl mx-auto animate-in fade-in duration-500">
          {children}
        </div>
      </main>

      {/* Overlay for mobile sidebar */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 md:hidden backdrop-blur-sm"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
      <AlertDialog open={gateOpen} onOpenChange={setGateOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Access Restricted</AlertDialogTitle>
            <AlertDialogDescription>
              Please complete the placement quiz to access this section.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Not now</AlertDialogCancel>
            <AlertDialogAction onClick={() => setLocation("/placement-quiz")}>
              Take placement quiz
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

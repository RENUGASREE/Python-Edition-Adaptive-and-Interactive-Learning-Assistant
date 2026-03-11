import { Switch, Route, Redirect, useLocation } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { useAuth } from "@/hooks/use-auth";
import { Loader2 } from "lucide-react";
import { AdaptiveProvider } from "@/context/AdaptiveContext";

// Pages
import Landing from "@/pages/Landing";
import Dashboard from "@/pages/Dashboard";
import Curriculum from "@/pages/Curriculum";
import LessonView from "@/pages/LessonView";
import NotFound from "@/pages/NotFound";
import Login from "@/pages/Login";
import Profile from "@/pages/Profile";
import Settings from "@/pages/Settings";
import Achievements from "@/pages/Achievements";
import PlacementQuiz from "@/pages/PlacementQuiz";
import ModuleQuiz from "@/pages/ModuleQuiz";
import Certificate from "@/pages/Certificate";
import Analytics from "@/pages/Analytics";

function ProtectedRoute({ component: Component }: { component: React.ComponentType }) {
  const { user, isLoading } = useAuth();
  const [location] = useLocation();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!user) {
    return <Redirect to="/signin" />;
  }

  const hasTakenQuiz = Boolean(user.has_taken_quiz || user.diagnostic_completed);
  if (!hasTakenQuiz) {
    const isDashboard = location === "/dashboard";
    const isPlacementQuiz = location === "/placement-quiz";
    const isLesson = location.startsWith("/lesson/");
    const isModuleQuiz = location.startsWith("/module/");
    const isCertificate = location.startsWith("/certificate/");
    const isCurriculum = location === "/curriculum";
    const isAchievements = location === "/achievements";
    const isAnalytics = location === "/analytics";
    if (
      !isDashboard &&
      !isPlacementQuiz &&
      (isLesson || isModuleQuiz || isCertificate || isCurriculum || isAchievements || isAnalytics)
    ) {
      try {
        localStorage.setItem("quizGateMessage", "Please complete the placement quiz first.");
      } catch {}
      return <Redirect to="/dashboard" />;
    }
  }

  return <Component />;
}

function Router() {
  const { user, isLoading } = useAuth();

  // Redirect logged-in users away from landing page
  if (isLoading) return null;

  return (
    <Switch>
      <Route path="/">
        {user ? <Redirect to="/dashboard" /> : <Landing />}
      </Route>
      
      <Route path="/signin">
        {user ? <Redirect to="/dashboard" /> : <Login />}
      </Route>

      <Route path="/login">
        <Redirect to="/signin" />
      </Route>
      
      <Route path="/dashboard">
        <ProtectedRoute component={Dashboard} />
      </Route>
      
      <Route path="/curriculum">
        <ProtectedRoute component={Curriculum} />
      </Route>
      
      <Route path="/lesson/:id">
        <ProtectedRoute component={LessonView} />
      </Route>

      <Route path="/placement-quiz">
        <ProtectedRoute component={PlacementQuiz} />
      </Route>

      <Route path="/module/:id/quiz">
        <ProtectedRoute component={ModuleQuiz} />
      </Route>

      <Route path="/certificate/:id">
        <ProtectedRoute component={Certificate} />
      </Route>

      <Route path="/profile">
        <ProtectedRoute component={Profile} />
      </Route>
      
      <Route path="/settings">
        <ProtectedRoute component={Settings} />
      </Route>

      <Route path="/achievements">
        <ProtectedRoute component={Achievements} />
      </Route>

      <Route path="/analytics">
        <ProtectedRoute component={Analytics} />
      </Route>

      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AdaptiveProvider>
        <TooltipProvider>
          <Router />
          <Toaster />
        </TooltipProvider>
      </AdaptiveProvider>
    </QueryClientProvider>
  );
}

export default App;

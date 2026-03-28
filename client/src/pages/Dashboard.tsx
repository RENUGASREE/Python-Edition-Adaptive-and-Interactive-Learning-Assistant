import { useAuth } from "@/hooks/use-auth";
import { useUserProgress } from "@/hooks/use-progress";
import { useModules } from "@/hooks/use-modules";
import { useMastery } from "@/hooks/use-mastery";
import { Layout } from "@/components/Layout";
import { Loader2, Flame, Award, BookOpen, ChevronRight, CheckCircle2 } from "lucide-react";
import { Link, useLocation } from "wouter";
import { useMemo } from "react";
import { Progress } from "@/components/ui/progress";

export default function Dashboard() {
  const { user } = useAuth();
  const { data: progress, isLoading: loadingProgress } = useUserProgress();
  const { data: modules, isLoading: loadingModules } = useModules();
  const { masteryVector, isLoading: loadingMastery } = useMastery();
  const [, setLocation] = useLocation();

  const placementCompleted = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);

  const stats = [
    { label: "Day Streak", value: user?.stats?.streak || 0, icon: Flame, color: "text-orange-500", bg: "bg-orange-500/10" },
    { label: "Total XP", value: user?.stats?.totalPoints || 0, icon: Award, color: "text-blue-500", bg: "bg-blue-500/10" },
    { label: "Lessons Done", value: user?.stats?.completedLessons || 0, icon: BookOpen, color: "text-green-500", bg: "bg-green-500/10" },
  ];

  const currentModule = useMemo(() => {
    if (!modules || !progress) return null;
    const lastIncomplete = progress.find(p => !p.completed);
    if (lastIncomplete) {
      return modules.find(m => m.lessons?.some(l => l.id === lastIncomplete.lessonId));
    }
    return modules[0];
  }, [modules, progress]);

  const moduleProgress = useMemo(() => {
    if (!modules || !progress) return [];
    return modules.map(m => {
      const lessons = m.lessons || [];
      const completed = lessons.filter(l => progress.find(p => p.lessonId === l.id && p.completed)).length;
      return {
        ...m,
        completedCount: completed,
        totalCount: lessons.length,
        percent: lessons.length > 0 ? (completed / lessons.length) * 100 : 0
      };
    });
  }, [modules, progress]);

  if (loadingProgress || loadingModules || loadingMastery) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-[60vh]">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8 max-w-5xl mx-auto">
        {/* Welcome Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 py-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Welcome back, {user?.firstName || user?.username}! 👋
            </h1>
            <p className="text-muted-foreground mt-1 text-lg">
              You've completed {user?.stats?.completedLessons || 0} lessons so far. Keep it up!
            </p>
          </div>
          <div className="flex gap-4">
            {stats.map((stat, i) => (
              <div key={i} className="bg-card border border-border p-4 rounded-2xl flex items-center gap-4 min-w-[140px]">
                <div className={`p-2 rounded-lg ${stat.bg} ${stat.color}`}>
                  <stat.icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-2xl font-bold leading-none">{stat.value}</div>
                  <div className="text-[10px] uppercase font-bold tracking-wider text-muted-foreground mt-1">{stat.label}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Banner */}
        <div className="bg-gradient-to-br from-primary/10 via-background to-background border border-primary/20 rounded-3xl p-8 relative overflow-hidden group">
          <div className="absolute -right-20 -top-20 w-64 h-64 bg-primary/5 rounded-full blur-3xl pointer-events-none" />
          
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
            <div className="max-w-xl">
              <h2 className="text-2xl font-bold mb-3">
                {!placementCompleted ? "Personalize your path" : "Continue your journey"}
              </h2>
              <p className="text-muted-foreground text-lg mb-6 leading-relaxed">
                {!placementCompleted 
                  ? "Take our quick assessment to skip what you already know and get a custom curriculum."
                  : currentModule 
                    ? `You're currently working on "${currentModule.title}". Pick up right where you left off.`
                    : "Ready to start your first lesson in Python?"}
              </p>
              <Link href={!placementCompleted ? "/placement-quiz" : "/curriculum"}>
                <button className="px-8 py-4 bg-primary text-primary-foreground font-bold rounded-2xl hover:scale-[1.02] transition-all shadow-xl shadow-primary/20 active:scale-95">
                  {!placementCompleted ? "Take Placement Quiz" : "Resume Learning"}
                </button>
              </Link>
            </div>
            {currentModule && (
              <div className="hidden lg:block bg-card/50 backdrop-blur-sm p-6 rounded-2xl border border-border w-72">
                <div className="text-xs font-bold uppercase text-primary mb-2">Current Module</div>
                <div className="font-bold text-lg leading-tight mb-4">{currentModule.title}</div>
                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-medium">
                    <span>Progress</span>
                    <span>{Math.round(moduleProgress.find(m => m.id === currentModule.id)?.percent || 0)}%</span>
                  </div>
                  <Progress value={moduleProgress.find(m => m.id === currentModule.id)?.percent || 0} className="h-2" />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Modules List */}
        <div className="grid md:grid-cols-2 gap-8 pt-4">
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-bold">Your Curriculum</h3>
              <Link href="/curriculum" className="text-sm font-medium text-primary hover:underline">View All</Link>
            </div>
            <div className="space-y-3">
              {moduleProgress.slice(0, 5).map((module) => (
                <Link key={module.id} href="/curriculum">
                  <div className="bg-card border border-border p-4 rounded-2xl hover:border-primary/50 transition-all cursor-pointer group flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold border-2 ${module.percent === 100 ? 'bg-primary/10 border-primary text-primary' : 'bg-muted border-transparent text-muted-foreground'}`}>
                        {module.percent === 100 ? <CheckCircle2 className="w-5 h-5" /> : module.order}
                      </div>
                      <div>
                        <div className="font-bold group-hover:text-primary transition-colors">{module.title}</div>
                        <div className="text-xs text-muted-foreground mt-0.5">{module.completedCount} / {module.totalCount} Lessons</div>
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              ))}
            </div>
          </div>

          <div className="space-y-6">
            <h3 className="text-xl font-bold">Mastery Snapshot</h3>
            <div className="bg-card border border-border p-6 rounded-3xl space-y-6">
              {Object.entries(masteryVector || {}).slice(0, 4).map(([topic, score]) => (
                <div key={topic} className="space-y-2">
                  <div className="flex justify-between text-sm font-medium">
                    <span className="capitalize">{topic.replace(/_/g, ' ')}</span>
                    <span className="text-primary">{Math.round(Number(score) * 100)}%</span>
                  </div>
                  <Progress value={Number(score) * 100} className="h-1.5" />
                </div>
              ))}
              {Object.keys(masteryVector || {}).length === 0 && (
                <div className="text-center py-8">
                  <div className="text-muted-foreground italic text-sm mb-4">No mastery data available yet.</div>
                  <Link href="/placement-quiz">
                    <button className="text-primary text-sm font-bold hover:underline">Complete diagnostic test →</button>
                  </Link>
                </div>
              )}
              {Object.keys(masteryVector || {}).length > 0 && (
                <div className="pt-4 text-center">
                  <Link href="/analytics">
                    <button className="text-xs font-bold text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                      View full analytics report →
                    </button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

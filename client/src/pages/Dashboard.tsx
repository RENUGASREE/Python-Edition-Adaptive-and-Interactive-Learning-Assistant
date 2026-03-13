import { useAuth } from "@/hooks/use-auth";
import { useProgress } from "@/hooks/use-progress";
import { useModules } from "@/hooks/use-modules";
import { useMastery } from "@/hooks/use-mastery";
import { useRecommendation } from "@/hooks/use-recommendation";
import { Layout } from "@/components/Layout";
import { Loader2, Flame, Award, Clock } from "lucide-react";
import { Link, useLocation } from "wouter";
import { useMemo, useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";
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
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

export default function Dashboard() {
  const { user } = useAuth();
  const { data: progress, isLoading: loadingProgress } = useProgress();
  const { data: modules, isLoading: loadingModules } = useModules();
  const { masteryVector, isLoading: loadingMastery } = useMastery();
  const { recommendation, isLoading: loadingRecommendation } = useRecommendation();
  const { toast } = useToast();
  const [, setLocation] = useLocation();
  const [gateOpen, setGateOpen] = useState(false);
  const [gateMessage, setGateMessage] = useState<string | null>(null);
  const { data: skillGaps } = useQuery({
    queryKey: ["/api/skill-gaps"],
    queryFn: async () => {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/skill-gaps/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch skill gaps");
      return res.json() as Promise<{ weak_topics: string[]; improving_topics: string[]; strong_topics: string[] }>;
    },
  });
  const { data: plan } = useQuery({
    queryKey: ["/api/learning-plan"],
    queryFn: async () => {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/learning-plan/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch plan");
      return res.json() as Promise<{ recommendedModules: number[]; recommendedLessons: number[]; reasoning: string }>;
    },
  });
  const { data: quizAttempts, isLoading: loadingQuizAttempts } = useQuery({
    queryKey: ["/api/quiz-attempts"],
    queryFn: async () => {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/quiz-attempts/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return [];
      if (!res.ok) throw new Error("Failed to fetch quiz attempts");
      return res.json();
    },
  });
  const parseModuleLevel = (notes?: string) => {
    if (!notes) return null;
    const match = notes.match(/module:(\d+):level:([A-Za-z]+)/i);
    if (!match) return null;
    return { moduleId: Number(match[1]), level: match[2] };
  };

  const normalizeLevel = (level?: string | null) => {
    if (!level) return "beginner";
    const lower = level.toLowerCase();
    if (lower === "advanced") return "pro";
    return lower;
  };

  const moduleLevels = useMemo(() => {
    const levels: Record<number, string> = {};
    (quizAttempts || []).forEach((attempt: any) => {
      const parsed = parseModuleLevel(attempt?.notes);
      if (parsed && parsed.moduleId) {
        levels[parsed.moduleId] = parsed.level;
      }
    });
    return levels;
  }, [quizAttempts]);

  const firstLessonId = useMemo(() => {
    const fallback = user?.level || "Beginner";
    const lessons = modules?.flatMap((m: any) => {
      const targetLevel = moduleLevels[m.id] || fallback;
      const filtered = (m.lessons || []).filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(targetLevel));
      const list = filtered.length > 0 ? filtered : (m.lessons || []);
      return list.map((l: any) => ({ ...l, moduleOrder: m.order }));
    }) || [];
    lessons.sort((a: any, b: any) => {
      if (a.moduleOrder !== b.moduleOrder) return a.moduleOrder - b.moduleOrder;
      return (a.order || 0) - (b.order || 0);
    });
    return lessons[0]?.id || 1;
  }, [modules, moduleLevels, user?.level]);

  if (loadingProgress || loadingModules || loadingQuizAttempts || loadingMastery || loadingRecommendation) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }
  if (!modules) {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center">
          <h1 className="text-2xl font-bold">Unable to load data. Please refresh.</h1>
        </div>
      </Layout>
    );
  }

  // Calculate stats
  const completedLessons = user?.stats?.completedLessons || 0;
  const totalLessons = modules?.reduce((acc, m) => acc + (m.lessons?.length || 0), 0) || 0;
  const progressPercent = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;
  const placementCompleted = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);
  const masteryEntries = Object.entries(masteryVector || {}).map(([topic, score]) => ({
    topic,
    score: Number(score),
  })).sort((a, b) => a.score - b.score);
  const weakestTopic = masteryEntries[0];
  const masteryColors = (score: number) => {
    if (score < 0.4) return "text-red-400";
    if (score < 0.7) return "text-yellow-400";
    return "text-green-400";
  };
  const moduleMastery = (modules || []).map((module: any) => {
    const lessonTopics = (module.lessons || [])
      .map((lesson: any) => lesson.topic || lesson.title)
      .filter(Boolean);
    const scores = lessonTopics
      .map((topic: string) => masteryVector?.[topic])
      .filter((value: any) => typeof value === "number") as number[];
    const avg = scores.length ? scores.reduce((acc, v) => acc + v, 0) / scores.length : 0;
    return { id: module.id, title: module.title, score: avg };
  });
  const recommendationReason = recommendation?.reason_for_recommendation || {};

  // Calculate Weekly Goal (Hours)
  const lessonDurations = new Map<number, number>();
  modules?.forEach(m => m.lessons?.forEach(l => lessonDurations.set(l.id, l.duration || 15))); // Default 15 mins

  let weeklyMinutes = 0;
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

  // Calculate Activity Data (Last 7 days)
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const activityMap = new Map<string, number>();
  days.forEach(d => activityMap.set(d, 0));

  progress?.forEach(p => {
    if (p.completed && p.completedAt) {
      const date = new Date(p.completedAt);
      
      // Weekly Goal Calculation
      if (date >= oneWeekAgo) {
        weeklyMinutes += lessonDurations.get(p.lessonId) || 0;
      }

      // Activity Chart Calculation (Simple Mon-Sun mapping for current week)
      // Ideally should be last 7 days relative to today, but fixed axis is easier for now
      const dayName = days[date.getDay()];
      activityMap.set(dayName, (activityMap.get(dayName) || 0) + (p.score || 10));
    }
  });
  
  const weeklyHours = (weeklyMinutes / 60).toFixed(1);
  const weeklyGoalTarget = user?.stats?.weeklyGoal || 5;
  const weeklyGoalPercent = Math.min((parseFloat(weeklyHours) / weeklyGoalTarget) * 100, 100);

  // Convert activity map to array for Recharts
  // Reorder to show Mon -> Sun if preferred, or just Sun -> Sat
  const activityData = [
    { day: 'Mon', score: activityMap.get('Mon') },
    { day: 'Tue', score: activityMap.get('Tue') },
    { day: 'Wed', score: activityMap.get('Wed') },
    { day: 'Thu', score: activityMap.get('Thu') },
    { day: 'Fri', score: activityMap.get('Fri') },
    { day: 'Sat', score: activityMap.get('Sat') },
    { day: 'Sun', score: activityMap.get('Sun') },
  ];

  useEffect(() => {
    try {
      const msg = localStorage.getItem("quizGateMessage");
      if (msg) {
        setGateMessage(msg);
        setGateOpen(true);
        localStorage.removeItem("quizGateMessage");
      }
    } catch {}
  }, []);

  return (
    <Layout>
      <AlertDialog open={gateOpen} onOpenChange={setGateOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Access Restricted</AlertDialogTitle>
            <AlertDialogDescription>
              {gateMessage || "Please complete the placement quiz to access this section."}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Not now</AlertDialogCancel>
            <AlertDialogAction onClick={() => setLocation("/placement-quiz")}>Take placement quiz</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      <div className="space-y-8">
        {!placementCompleted && (
          <div className="bg-card border border-primary/40 rounded-2xl p-6 shadow-lg shadow-primary/15">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold">Start Your Learning Journey</h2>
                <p className="text-muted-foreground mt-1">
                  To personalize your learning path, you must complete the placement quiz.
                </p>
              </div>
              <Link href="/placement-quiz">
                <button className="px-6 py-3 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-colors">
                  Take Placement Quiz
                </button>
              </Link>
            </div>
          </div>
        )}
        {/* Welcome Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-display font-bold text-foreground">
              Welcome back, {user?.firstName || 'Coder'}! 👋
            </h1>
            <p className="text-muted-foreground mt-1">Ready to continue your Python journey?</p>
          </div>
          <div className="flex gap-4">
            <StatBadge icon={Flame} value={String(user?.stats?.streak || 0)} label="Day Streak" color="text-orange-500" bg="bg-orange-500/10" />
            <StatBadge icon={Award} value={String(user?.stats?.totalPoints || 0)} label="XP" color="text-accent" bg="bg-accent/10" />
          </div>
        </div>

        {/* Continue Learning */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 bg-gradient-to-br from-card to-card/50 border border-border rounded-2xl p-6 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-primary/10 transition-colors" />
            
            <h2 className="text-xl font-bold mb-2 z-10 relative">
              {!placementCompleted ? "Start with the placement quiz" : completedLessons === 0 ? "Start with Module 1: Introduction" : "Continue your journey"}
            </h2>
            <p className="text-muted-foreground mb-6 max-w-md z-10 relative">
              {!placementCompleted
                ? "Take a quick quiz so we can personalize your learning path."
                : completedLessons === 0 
                ? "Begin your Python adventure by learning about variables and data types."
                : "Great job! Keep going to master more Python concepts."}
            </p>
            
            <Link href={!placementCompleted ? "/placement-quiz" : completedLessons === 0 ? `/lesson/${firstLessonId}` : `/lesson/${progress?.find(p => !p.completed)?.lessonId || firstLessonId}`}>
              <button className="px-6 py-3 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-colors z-10 relative shadow-lg shadow-primary/20 hover:translate-y-[-2px] active:translate-y-0">
                {!placementCompleted ? "Take placement quiz" : completedLessons === 0 ? "Start First Lesson" : "Continue Lesson"}
              </button>
            </Link>
          </div>

          <div className="bg-card border border-border rounded-2xl p-6 flex flex-col justify-between">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-muted-foreground" />
              <span className="font-medium text-muted-foreground">Weekly Goal</span>
            </div>
            <div className="text-3xl font-bold font-display mb-2">{weeklyHours} / {weeklyGoalTarget} hrs</div>
            <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
              <div className="h-full bg-accent" style={{ width: `${weeklyGoalPercent}%` }} />
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground mb-2">Recommended Next Lesson</div>
            <div className="text-xl font-semibold">
              {recommendation?.recommended_lesson_title || recommendation?.next_topic || "Take diagnostic quiz"}
            </div>
            <div className="text-sm text-muted-foreground mt-2">
              {recommendation?.reason_for_recommendation
                ? `Priority score ${recommendationReason.priority_score ?? ""}`
                : "Complete more learning activities to personalize recommendations."}
            </div>
            <div className="text-xs text-muted-foreground mt-3">
              Difficulty {recommendation?.difficulty_level || "Beginner"}
            </div>
            <div className="text-xs text-muted-foreground mt-3">
              Confidence {Math.round((recommendation?.confidence_score || 0) * 100)}%
            </div>
            {recommendation?.reasons && recommendation.reasons.length > 0 && (
              <div className="mt-4">
                <div className="text-sm font-medium mb-2">Why this lesson was recommended</div>
                <ul className="list-disc pl-5 text-sm text-muted-foreground space-y-1">
                  {recommendation.reasons.map((r, idx) => (
                    <li key={idx}>{r}</li>
                  ))}
                </ul>
              </div>
            )}
            {recommendation?.reason_for_recommendation && (
              <div className="mt-4 space-y-2 text-xs text-muted-foreground">
                <div className="flex justify-between">
                  <span>Mastery gap</span>
                  <span>{Math.round((1 - (recommendationReason.mastery || 0)) * 100)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Recent failures</span>
                  <span>{Math.round((recommendationReason.recent_failure_rate || 0) * 100)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Prerequisite weight</span>
                  <span>{Math.round((recommendationReason.prerequisite_dependency_weight || 0) * 100)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Engagement factor</span>
                  <span>{Math.round((recommendationReason.engagement_factor || 0) * 100)}%</span>
                </div>
              </div>
            )}
          </div>

          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground mb-2">Weakest Topic</div>
            <div className={`text-xl font-semibold ${masteryColors(weakestTopic?.score || 0)}`}>
              {weakestTopic?.topic || "No mastery yet"}
            </div>
            <div className="text-sm text-muted-foreground mt-2">
              Mastery {Math.round((weakestTopic?.score || 0) * 100)}%
            </div>
          </div>

          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground mb-4">Mastery Snapshot</div>
            <div className="space-y-3">
              {masteryEntries.slice(0, 3).map((entry) => (
                <div key={entry.topic} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span>{entry.topic}</span>
                    <span className={masteryColors(entry.score)}>{Math.round(entry.score * 100)}%</span>
                  </div>
                  <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: `${Math.round(entry.score * 100)}%` }} />
                  </div>
                </div>
              ))}
              {masteryEntries.length === 0 && (
                <div className="text-sm text-muted-foreground">Complete the diagnostic quiz to begin.</div>
              )}
            </div>
          </div>
        </div>

        {/* Progress & Modules */}
        <div className="grid lg:grid-cols-2 gap-8">
          <div className="bg-card border border-border rounded-2xl p-6">
            <h3 className="text-lg font-bold mb-4">Skill Gap Analysis</h3>
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm font-medium mb-2">Weak Areas</div>
                <ul className="text-sm text-muted-foreground space-y-1">
                  {(skillGaps?.weak_topics || []).map((t) => <li key={`w-${t}`}>{t}</li>)}
                  {(skillGaps?.weak_topics || []).length === 0 && <li className="opacity-60">None</li>}
                </ul>
              </div>
              <div>
                <div className="text-sm font-medium mb-2">Improving</div>
                <ul className="text-sm text-muted-foreground space-y-1">
                  {(skillGaps?.improving_topics || []).map((t) => <li key={`i-${t}`}>{t}</li>)}
                  {(skillGaps?.improving_topics || []).length === 0 && <li className="opacity-60">None</li>}
                </ul>
              </div>
              <div>
                <div className="text-sm font-medium mb-2">Strong</div>
                <ul className="text-sm text-muted-foreground space-y-1">
                  {(skillGaps?.strong_topics || []).map((t) => <li key={`s-${t}`}>{t}</li>)}
                  {(skillGaps?.strong_topics || []).length === 0 && <li className="opacity-60">None</li>}
                </ul>
              </div>
            </div>
          </div>
          <div className="bg-card border border-border rounded-2xl p-6">
            <h3 className="text-lg font-bold mb-2">Your Personalized Learning Plan</h3>
            <div className="text-sm text-muted-foreground mb-3">{plan?.reasoning || "Complete activities to generate a plan."}</div>
            <div className="text-sm">
              <div className="font-medium mb-1">Recommended Next Steps</div>
              <ul className="list-decimal pl-5 space-y-1">
                {(plan?.recommendedLessons || []).slice(0, 5).map((id) => (
                  <li key={`rl-${id}`}>
                    <Link href={`/lesson/${id}`}>Lesson {id}</Link>
                  </li>
                ))}
                {(plan?.recommendedLessons || []).length === 0 && <li className="text-muted-foreground">No recommendations yet</li>}
              </ul>
            </div>
          </div>
          {/* Recent Activity Chart */}
          <div className="bg-card border border-border rounded-2xl p-6">
            <h3 className="text-lg font-bold mb-6">Learning Activity</h3>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={activityData}>
                  <XAxis 
                    dataKey="day" 
                    stroke="#64748b" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false} 
                  />
                  <YAxis hide />
                  <Tooltip 
                    cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                    contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                  />
                  <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                    {activityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={index === 4 ? 'hsl(var(--primary))' : 'hsl(var(--muted))'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Module Mastery */}
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold">Module Mastery</h3>
              <Link href="/curriculum" className="text-sm text-primary hover:underline">View All</Link>
            </div>

            <div className="space-y-4">
              {moduleMastery.slice(0, 4).map((module: any) => (
                <div key={module.id} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>{module.title}</span>
                    <span className={masteryColors(module.score)}>{Math.round(module.score * 100)}%</span>
                  </div>
                  <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: `${Math.round(module.score * 100)}%` }} />
                  </div>
                </div>
              ))}
              {moduleMastery.length === 0 && (
                <div className="text-sm text-muted-foreground">Complete lessons to see module mastery.</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

function StatBadge({ icon: Icon, value, label, color, bg }: { icon: any, value: string, label: string, color: string, bg: string }) {
  return (
    <div className={`flex items-center gap-3 px-4 py-2 rounded-xl border border-border/50 bg-card`}>
      <div className={`p-2 rounded-lg ${bg} ${color}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div>
        <div className="font-bold text-lg leading-none">{value}</div>
        <div className="text-[10px] text-muted-foreground uppercase font-medium tracking-wider">{label}</div>
      </div>
    </div>
  );
}

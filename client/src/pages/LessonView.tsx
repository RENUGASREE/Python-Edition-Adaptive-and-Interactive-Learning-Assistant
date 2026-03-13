import { useParams, Link } from "wouter";
import { useLesson, useRunChallenge } from "@/hooks/use-lessons";
import { useProgress, useUpdateProgress } from "@/hooks/use-progress";
import { useAuth } from "@/hooks/use-auth";
import { Loader2, Play, ChevronRight, AlertCircle, RotateCcw, Code2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Editor } from "@/components/Editor";
import { useMastery } from "@/hooks/use-mastery";
import { useMasteryUpdate } from "@/hooks/use-mastery-update";
import { useState, useEffect, useMemo, Suspense, lazy } from "react";
import confetti from "canvas-confetti";
import { useToast } from "@/hooks/use-toast";
import { useQuery } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { useModules } from "@/hooks/use-modules";
import { Layout } from "@/components/Layout";

const ChatTutor = lazy(() => import("@/components/ChatTutor").then((mod) => ({ default: mod.ChatTutor })));

export default function LessonView() {
  const { id } = useParams();
  const lessonId = Number(id);
  const { data: lesson, isLoading } = useLesson(lessonId);
  const { data: modules, isLoading: loadingModules } = useModules();
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
  const { data: progress, isLoading: loadingProgress } = useProgress();
  const runMutation = useRunChallenge();
  const progressMutation = useUpdateProgress();
  const { user } = useAuth();
  const { toast } = useToast();
  const { masteryVector } = useMastery();
  const masteryUpdate = useMasteryUpdate();

  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [masteryImpact, setMasteryImpact] = useState<number | null>(null);
  const masteryKey = (lesson as any)?.topic || lesson?.title;
  const masteryScore = masteryKey ? (masteryVector?.[masteryKey] ?? 0) : 0;
  const encouragement =
    masteryScore < 0.4
      ? "Let’s strengthen fundamentals before moving ahead."
      : masteryScore > 0.8
      ? "Try advanced challenges to deepen mastery."
      : "Keep building confidence with structured practice.";

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

  const placementCompleted = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);
  const allLessons = useMemo(() => {
    if (!modules) return [];
    const fallback = user?.level || "Beginner";
    return (modules as any[])
      .flatMap((m: any) => {
        const targetLevel = moduleLevels[m.id] || fallback;
        const filtered = (m.lessons || []).filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(targetLevel));
        const lessons = filtered.length > 0 ? filtered : (m.lessons || []);
        return lessons.map((l: any) => ({ ...l, moduleOrder: m.order }));
      })
      .sort((a, b) => {
        if (a.moduleOrder !== b.moduleOrder) return a.moduleOrder - b.moduleOrder;
        return (a.order || 0) - (b.order || 0);
      });
  }, [modules, moduleLevels, user?.level]);
  const firstLessonId = allLessons[0]?.id || 1;

  const isLessonCompleted = (id: number) => {
    return progress?.find(p => p.lessonId === id)?.completed;
  };

  const isModuleCompleted = (moduleId: number) => {
    const module = (modules as any[])?.find(m => m.id === moduleId);
    if (!module || !module.lessons || module.lessons.length === 0) return false;
    const fallback = user?.level || "Beginner";
    const targetLevel = moduleLevels[moduleId] || fallback;
    const filtered = (module.lessons as any[]).filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(targetLevel));
    const lessons = filtered.length > 0 ? filtered : (module.lessons as any[]);
    return lessons.every(l => isLessonCompleted(l.id));
  };

  const isModuleLocked = (moduleId: number) => {
    const module = (modules as any[])?.find(m => m.id === moduleId);
    if (!module || module.order === 1) return false;
    const previousModule = (modules as any[])?.find(m => m.order === module.order - 1);
    return previousModule ? !isModuleCompleted(previousModule.id) : false;
  };

  const isLessonLocked = (id: number) => {
    const lessonIndex = allLessons.findIndex(l => l.id === id);
    if (lessonIndex <= 0) {
      const lesson = allLessons[0];
      if (!lesson) return false;
      if (isModuleLocked(lesson.moduleId)) return true;
      return !placementCompleted;
    }
    const previousLesson = allLessons[lessonIndex - 1];
    return !isLessonCompleted(previousLesson.id);
  };

  const lessonSections = useMemo(() => {
    const raw = lesson?.content || "";
    const chunks = raw.split("\n\n").map((chunk) => chunk.trim()).filter(Boolean);
    const explanation = chunks[0] || "Review the explanation and key idea for this topic.";
    const codeMatch = raw.match(/```(?:python)?\n([\s\S]*?)```/);
    const codeBlock = codeMatch?.[1]?.trim() || "print('Hello, Python!')";
    return {
      explanation,
      syntax: codeBlock,
      example: codeBlock,
      practice: lesson?.challenges?.[0]?.description || "Complete the practice challenge to solidify mastery.",
    };
  }, [lesson]);

  // Initialize code when lesson loads
  useEffect(() => {
    if (lesson?.challenges?.[0]) {
      setCode(lesson.challenges[0].initialCode);
    }
  }, [lesson]);

  const handleRun = async () => {
    if (!lesson?.challenges?.[0]) return;
    
    setOutput("Running...");
    setError(null);
    
    try {
      const result = await runMutation.mutateAsync({
        id: lesson.challenges[0].id,
        code
      });
      
      setOutput(result.output);
      
      if (result.error) {
        setError(result.error);
      } else if (result.passed) {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
        toast({
          title: "Challenge Passed!",
          description: "Great job! Your solution is correct.",
          className: "bg-green-500 text-white border-none",
        });
        setMasteryImpact(0.06);
        
        // Mark lesson as complete
        if (user) {
          progressMutation.mutate({
            userId: user.id,
            lessonId,
            completed: true,
            lastCode: code,
            score: 100,
            completedAt: new Date()
          });
        }
      } else {
        setError("Code ran but didn't pass all test cases.");
      }
    } catch (err: any) {
      console.error("Run challenge error:", err);
      setError(err.message || "Failed to execute code");
      setOutput("");
    }
  };

  if (isLoading || loadingModules || loadingQuizAttempts || loadingProgress) {
    return (
      <div className="flex items-center justify-center h-screen bg-background text-primary">
        <Loader2 className="w-10 h-10 animate-spin" />
      </div>
    );
  }
  if (!lesson) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[70vh] px-4">
          <div className="max-w-lg w-full bg-card border border-border rounded-2xl p-8 text-center space-y-4">
            <h1 className="text-2xl font-bold">Unable to load lesson content</h1>
            <p className="text-muted-foreground">Please try again.</p>
            <button onClick={() => window.location.reload()} className="px-4 py-2 bg-primary text-primary-foreground rounded-lg">
              Retry
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  if (!placementCompleted && lessonId === firstLessonId) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[70vh] px-4">
          <div className="max-w-lg w-full bg-card border border-border rounded-2xl p-8 text-center space-y-4">
            <h1 className="text-2xl font-bold">Placement quiz required</h1>
            <p className="text-muted-foreground">Complete the placement quiz to unlock your first lesson.</p>
            <Link href="/placement-quiz">
              <button className="px-6 py-3 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-colors">
                Take placement quiz
              </button>
            </Link>
          </div>
        </div>
      </Layout>
    );
  }
  
  if (isLessonLocked(lessonId)) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[70vh] px-4">
          <div className="max-w-lg w-full bg-card border border-border rounded-2xl p-8 text-center space-y-4">
            <h1 className="text-2xl font-bold">Lesson locked</h1>
            <p className="text-muted-foreground">Complete the previous lesson to unlock this content.</p>
            <Link href="/curriculum">
              <button className="px-6 py-3 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-colors">
                Go to curriculum
              </button>
            </Link>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden">
      {/* Header */}
      <header className="h-16 border-b border-border flex items-center justify-between px-6 bg-card shrink-0 z-20">
        <div className="flex items-center gap-4">
          <Link href="/curriculum" className="p-2 hover:bg-muted rounded-lg transition-colors">
            <ChevronRight className="w-5 h-5 rotate-180" />
          </Link>
          <div>
            <h1 className="font-bold text-lg leading-tight">{lesson.title}</h1>
            <p className="text-xs text-muted-foreground">{lesson.module.title}</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
           {/* Progress Indicator */}
           <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted/50 px-3 py-1.5 rounded-full">
             <span>Level: {lesson.difficulty}</span>
           </div>
        </div>
      </header>

      {/* Main Content Split */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Pane: Content */}
        <div className="w-1/2 border-r border-border bg-card/30 overflow-y-auto p-8 scrollbar-thin">
          <div className="max-w-2xl mx-auto markdown-content">
            <div className="mb-6 p-4 rounded-xl border border-border bg-card">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <div className="text-sm text-muted-foreground">Mastery for this topic</div>
                  <div className="text-xl font-semibold">{Math.round(masteryScore * 100)}%</div>
                </div>
                <button
                  onClick={() => masteryUpdate.mutate({ moduleId: (lesson as any).moduleId, score: 0.9, source: "understood", topic: masteryKey })}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium"
                >
                  Mark as Understood
                </button>
              </div>
              <div className="text-sm text-muted-foreground mt-3">{encouragement}</div>
              <div className="text-xs text-muted-foreground mt-2">
                Updated mastery estimate: {Math.round(masteryScore * 100)}%
                {masteryImpact ? ` · Impact +${Math.round(masteryImpact * 100)}%` : ""}
              </div>
            </div>
             <div className="grid md:grid-cols-2 gap-4 mb-6">
               <div className="p-4 rounded-xl border border-border bg-card">
                 <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Explanation</div>
                 <div className="text-sm text-muted-foreground">{lessonSections.explanation}</div>
               </div>
               <div className="p-4 rounded-xl border border-border bg-card">
                 <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Syntax</div>
                 <pre className="text-xs bg-muted/50 rounded-lg p-3 overflow-x-auto">{lessonSections.syntax}</pre>
               </div>
               <div className="p-4 rounded-xl border border-border bg-card">
                 <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Example</div>
                 <pre className="text-xs bg-muted/50 rounded-lg p-3 overflow-x-auto">{lessonSections.example}</pre>
               </div>
               <div className="p-4 rounded-xl border border-border bg-card">
                 <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Practice</div>
                 <div className="text-sm text-muted-foreground">{lessonSections.practice}</div>
               </div>
             </div>
             <ReactMarkdown>{lesson.content}</ReactMarkdown>
            
            {(lesson as any)?.quizzes?.length > 0 && (
              <div className="mt-8 p-6 border border-border rounded-xl bg-card">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold">Lesson Quiz</h3>
                  {String((lesson as any).quizzes?.[0]?.title || "").includes("AI Generated") && (
                    <div className="text-xs px-2 py-1 rounded bg-accent/10 text-accent border border-accent/30">
                      AI Generated Quiz
                    </div>
                  )}
                </div>
                <div className="mt-4 space-y-4">
                  {((lesson as any).quizzes?.[0]?.questions || []).map((q: any, idx: number) => (
                    <div key={`q-${idx}`} className="space-y-2">
                      <div className="font-medium">{idx + 1}. {q.text}</div>
                      <div className="grid gap-2">
                        {(q.options || []).map((opt: any, i: number) => (
                          <label key={`q-${idx}-o-${i}`} className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:border-primary/60">
                            <input type="radio" name={`ai-quiz-q-${idx}`} disabled />
                            <span>{opt.text}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
             
             {lesson.challenges?.[0] && (
               <div className="mt-8 p-6 bg-primary/5 border border-primary/20 rounded-xl">
                 <h3 className="text-lg font-bold text-primary mb-2 flex items-center gap-2">
                   <Code2 className="w-5 h-5" /> Challenge
                 </h3>
                 <ReactMarkdown>{lesson.challenges[0].description}</ReactMarkdown>
               </div>
             )}
          </div>
        </div>

        {/* Right Pane: Code Editor */}
        <div className="w-1/2 flex flex-col bg-[#1e1e1e]">
          {/* Toolbar */}
          <div className="h-12 bg-[#252526] border-b border-[#333] flex items-center justify-between px-4 shrink-0">
             <div className="flex items-center gap-2">
               <div className="px-3 py-1 bg-[#37373d] text-xs text-white rounded">main.py</div>
             </div>
             
             <div className="flex items-center gap-2">
               <button 
                 onClick={() => setCode(lesson.challenges?.[0]?.initialCode || "")}
                 className="p-1.5 text-muted-foreground hover:text-white hover:bg-[#37373d] rounded transition-colors"
                 title="Reset Code"
               >
                 <RotateCcw className="w-4 h-4" />
               </button>
               <button
                 onClick={handleRun}
                 disabled={runMutation.isPending}
                 className="flex items-center gap-2 px-4 py-1.5 bg-primary hover:bg-primary/90 text-primary-foreground text-xs font-bold rounded transition-all disabled:opacity-50"
               >
                 {runMutation.isPending ? <Loader2 className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3 fill-current" />}
                 Run Code
               </button>
             </div>
          </div>

          {/* Editor Area */}
          <div className="flex-1 overflow-hidden relative">
            <Editor 
              code={code} 
              onChange={setCode}
            />
          </div>

          {/* Console / Output */}
          <div className="h-1/3 border-t border-[#333] bg-[#0f0f0f] flex flex-col shrink-0">
            <div className="h-8 bg-[#1e1e1e] border-b border-[#333] px-4 flex items-center text-xs font-mono text-muted-foreground uppercase tracking-wider">
              Console Output
            </div>
            <div className="flex-1 p-4 font-mono text-sm overflow-auto">
              {error ? (
                 <div className="text-red-400 whitespace-pre-wrap flex gap-2">
                   <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                   {error}
                 </div>
              ) : output ? (
                 <div className="text-green-400 whitespace-pre-wrap">{output}</div>
              ) : (
                 <div className="text-gray-600 italic">Run your code to see output...</div>
              )}
            </div>
          </div>
        </div>
      </div>

      <Suspense fallback={null}>
        <ChatTutor lessonId={lessonId} lessonTitle={lesson.title} lessonContent={lesson.content} />
      </Suspense>
    </div>
  );
}

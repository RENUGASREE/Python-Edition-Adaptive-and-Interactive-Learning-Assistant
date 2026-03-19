import { useParams, Link } from "wouter";
import { useLesson, useRunChallenge } from "@/hooks/use-lessons";
import { useUserProgress, useUpdateProgress } from "@/hooks/use-progress";
import { useAuth } from "@/hooks/use-auth";
import { Loader2, Play, ChevronRight, AlertCircle, RotateCcw, Code2, Bot, Sparkles, X } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Editor } from "@/components/Editor";
import { useMastery } from "@/hooks/use-mastery";
import { useMasteryUpdate } from "@/hooks/use-mastery-update";
import { useState, useEffect, useMemo, Suspense, lazy } from "react";
import confetti from "canvas-confetti";
import { useToast } from "@/hooks/use-toast";
import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useModules } from "@/hooks/use-modules";
import { Layout } from "@/components/Layout";
import { cn } from "@/lib/utils";
import QuizView from "@/components/QuizView";

const ChatTutor = lazy(() => import("@/components/ChatTutor").then((mod) => ({ default: mod.ChatTutor })));

export default function LessonView() {
  const { id } = useParams();
  const lessonId = Number(id);
  const { data: lesson, isLoading, error: lessonFetchError, refetch } = useLesson(lessonId);
  const { data: modules, isLoading: loadingModules } = useModules();
  const { data: quizAttempts, isLoading: loadingQuizAttempts } = useQuery({
    queryKey: ["/api/quiz-attempts"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/quiz-attempts/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return [];
      if (!res.ok) throw new Error("Failed to fetch quiz attempts");
      return res.json();
    },
  });
  const { data: progress, isLoading: loadingProgress } = useUserProgress();
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

  const currentLessonIndex = allLessons.findIndex(l => l.id === lessonId);
  const prevLessonId = currentLessonIndex > 0 ? allLessons[currentLessonIndex - 1].id : null;
  const nextLessonId = currentLessonIndex >= 0 && currentLessonIndex < allLessons.length - 1 ? allLessons[currentLessonIndex + 1].id : null;

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
    // If it's the current lesson and the API says it's unlocked, trust it.
    if (id === lessonId && lesson && typeof (lesson as any).unlocked !== 'undefined') {
      return !(lesson as any).unlocked;
    }

    const lessonIndex = allLessons.findIndex(l => l.id === id);
    if (lessonIndex <= 0) {
      const firstLesson = allLessons[0];
      if (!firstLesson) return false;
      if (id === firstLesson.id) {
        if (isModuleLocked(firstLesson.moduleId)) return true;
        return !placementCompleted;
      }
      // If not the first lesson and not found in allLessons, something is wrong with level filtering.
      // Default to checking if the lesson's module is locked.
      const l = modules?.flatMap((m: any) => m.lessons || []).find((l: any) => l.id === id);
      if (l && isModuleLocked(l.moduleId)) return true;
      return false;
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

  // Initialize code when lesson loads - empty by default to encourage active learning
  useEffect(() => {
    if (lesson?.challenges?.[0]) {
      setCode("");
    }
  }, [lesson]);

  const [quizResults, setQuizResults] = useState<Record<string, { selected: number; correct: boolean }>>({});

  const handleRun = async () => {
    if (!lesson?.challenges?.[0]) return;
    
    setOutput("Running...");
    setError(null);
    
    try {
      const result = await runMutation.mutateAsync({
        id: lesson.challenges[0].id,
        code: code.trim() || ""
      });
      
      setOutput(result.output || "");
      
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
  const lessonErrorStatus = (lessonFetchError as any)?.status;
  const lessonErrorMessage = (lessonFetchError as any)?.message || "Unable to load lesson content";

  if (!lesson) {
    let title = "Unable to load lesson content";
    let description = "Please try again.";
    let action: React.ReactNode = (
      <button
        onClick={() => refetch()}
        className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
      >
        Retry
      </button>
    );

    if (lessonErrorStatus === 401) {
      title = "Authentication required";
      description = "Please sign in to access lessons.";
      action = (
        <button
          onClick={() => (window.location.href = "/login")}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
        >
          Go to login
        </button>
      );
    } else if (lessonErrorStatus === 403) {
      title = "Placement quiz required";
      description = "Complete the placement test to unlock this lesson.";
      action = (
        <button
          onClick={() => (window.location.href = "/placement-quiz")}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
        >
          Take the placement quiz
        </button>
      );
    } else if (lessonErrorStatus === 404) {
      title = "Lesson not found";
      description = "This lesson may have been removed or does not exist.";
    }

    return (
      <Layout>
        <div className="flex items-center justify-center min-h-[70vh] px-4">
          <div className="max-w-lg w-full bg-card border border-border rounded-2xl p-8 text-center space-y-4">
            <h1 className="text-2xl font-bold">{title}</h1>
            <p className="text-muted-foreground">{description}</p>
            <p className="text-xs text-muted-foreground">{lessonErrorMessage}</p>
            {action}
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
           <div className="flex items-center gap-2 mr-4">
             {prevLessonId && (
               <Link href={`/lesson/${prevLessonId}`}>
                 <button className="p-2 hover:bg-muted rounded-lg transition-colors border border-border flex items-center gap-1 text-sm font-medium" title="Previous Lesson">
                   <ChevronRight className="w-4 h-4 rotate-180" />
                   <span>Previous</span>
                 </button>
               </Link>
             )}
             {nextLessonId && (
               <Link href={`/lesson/${nextLessonId}`}>
                 <button 
                   disabled={!isLessonCompleted(lessonId)}
                   className="p-2 hover:bg-muted rounded-lg transition-colors border border-border flex items-center gap-1 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed" 
                   title={isLessonCompleted(lessonId) ? "Next Lesson" : "Complete challenge to unlock next lesson"}
                 >
                   <span>Next</span>
                   <ChevronRight className="w-4 h-4" />
                 </button>
               </Link>
             )}
           </div>
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
             
             <ReactMarkdown>{lesson.content}</ReactMarkdown>
            
            {(lesson as any)?.quizzes?.length > 0 && (
              <div className="mt-12 p-8 border border-border rounded-2xl bg-card shadow-sm">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-xl font-bold tracking-tight">Check Your Knowledge</h3>
                    <p className="text-sm text-muted-foreground mt-1">Select the correct option for each question to test your understanding.</p>
                  </div>
                  <Bot className="w-5 h-5 text-primary opacity-50" />
                </div>
                <QuizView
                  questions={(lesson as any).quizzes?.[0]?.questions || []}
                  onSubmit={async (answers) => {
                    try {
                      // Calculate score
                      const questions = (lesson as any).quizzes?.[0]?.questions || [];
                      const correctCount = questions.reduce((acc: number, q: any) => {
                        const selectedIdx = answers[q.id];
                        const isCorrect = q.options?.[selectedIdx]?.correct;
                        return isCorrect ? acc + 1 : acc;
                      }, 0);
                      const score = (correctCount / questions.length) * 100;

                      await progressMutation.mutateAsync({
                        lessonId: parseInt(lessonId),
                        completed: true,
                        score: score,
                        lastCode: JSON.stringify(answers)
                      });
                      
                      toast({
                        title: "Knowledge Check Completed",
                        description: `You scored ${Math.round(score)}%`,
                      });
                      
                      confetti({
                        particleCount: 100,
                        spread: 70,
                        origin: { y: 0.6 }
                      });
                    } catch (err: any) {
                      toast({
                        title: "Error",
                        description: err.message || "Failed to save progress",
                        variant: "destructive",
                      });
                    }
                  }}
                />
              </div>
            )}
             
             {lesson.challenges?.[0] && (
               <div className="mt-12 p-6 bg-primary/5 border border-primary/20 rounded-2xl relative overflow-hidden group">
                 <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                   <Code2 className="w-16 h-16" />
                 </div>
                 <h3 className="text-lg font-bold text-primary mb-3 flex items-center gap-2">
                   <Sparkles className="w-5 h-5" /> Active Learning Challenge
                 </h3>
                 <div className="markdown-content prose prose-sm dark:prose-invert max-w-none">
                   <ReactMarkdown>{lesson.challenges[0].description}</ReactMarkdown>
                 </div>
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

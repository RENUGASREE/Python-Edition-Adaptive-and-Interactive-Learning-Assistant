import { useParams, Link, useLocation } from "wouter";
import { useLesson, useRunChallenge } from "@/hooks/use-lessons";
import { useUserProgress, useUpdateProgress } from "@/hooks/use-progress";
import { useAuth } from "@/hooks/use-auth";
import { Loader2, Play, ChevronRight, AlertCircle, RotateCcw, Code2, Bot, Sparkles, X, Target, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";
import { formatConsoleOutput, getConsoleHelpText } from "@/lib/console-formatter";
import { Editor } from "@/components/Editor";
import { TerminalConsole, InteractiveConsole } from "@/components/TerminalConsole";
import { useMastery } from "@/hooks/use-mastery";
import { useMasteryUpdate } from "@/hooks/use-mastery-update";
import { useState, useEffect, useMemo, Suspense, lazy } from "react";
import confetti from "canvas-confetti";
import { useToast } from "@/hooks/use-toast";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useModules } from "@/hooks/use-modules";
import { Layout } from "@/components/Layout";
import { cn } from "@/lib/utils";
import QuizView from "@/components/QuizView";
import { parseInputCalls, getInputCount, formatInteractiveOutput, stripInputPromptsFromOutput } from "@/lib/interactive-console";

const ChatTutor = lazy(() => import("@/components/ChatTutor").then((mod) => ({ default: mod.ChatTutor })));

export default function LessonView() {
  const { id } = useParams();
  const [, setLocation] = useLocation();
  const queryClient = useQueryClient();
  const lessonId = id || "";
  
  // CRITICAL: Force refetch user data on mount to ensure fresh masteryVector after quiz
  useEffect(() => {
    queryClient.refetchQueries({ queryKey: ["/api/auth/user"], exact: true });
  }, [queryClient]);
  
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
  
  // Interactive console state
  const [isInteractiveMode, setIsInteractiveMode] = useState(false);
  const [isWaitingForInput, setIsWaitingForInput] = useState(false);
  const [collectedInputs, setCollectedInputs] = useState<string[]>([]);
  const [inputCalls, setInputCalls] = useState<any[]>([]);
  const [currentInputIndex, setCurrentInputIndex] = useState(0);
  const [interactiveOutput, setInteractiveOutput] = useState("");
  const [totalInputsNeeded, setTotalInputsNeeded] = useState(0)
  const [isCompleted, setIsCompleted] = useState(false);
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
    const match = notes.match(/module:([^:]+):level:([A-Za-z]+)/i);
    if (!match) return null;
    return { moduleId: match[1], level: match[2] };
  };

  const normalizeLevel = (level?: string | null) => {
    if (!level) return "beginner";
    const lower = level.toLowerCase();
    if (lower === "advanced") return "pro";
    return lower;
  };

  const moduleLevels = useMemo(() => {
    const levels: Record<string, string> = {};

    const mvDiffs = (user as any)?.masteryVector?._module_difficulty || {};
    Object.entries(mvDiffs).forEach(([key, val]) => {
      levels[key] = val as string;
      if (typeof key === "string" && key.includes("_")) {
        levels[key.replace(/_/g, "-")] = val as string;
      }
    });

    if (levels["mod-introduction"] || levels["mod_introduction"]) {
      levels["mod-python-basics"] = levels["mod-introduction"] || levels["mod_introduction"];
    }

    (quizAttempts || []).forEach((attempt: any) => {
      const parsed = parseModuleLevel(attempt?.notes);
      if (parsed && parsed.moduleId) {
        levels[parsed.moduleId] = parsed.level;
      }
    });
    return levels;
  }, [quizAttempts, user]);

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
  const firstLessonId = allLessons[0]?.id || "";

  const currentLessonIndex = allLessons.findIndex(l => l.id === lessonId);
  const prevLessonId = currentLessonIndex > 0 ? allLessons[currentLessonIndex - 1].id : null;
  const nextLessonId = currentLessonIndex >= 0 && currentLessonIndex < allLessons.length - 1 ? allLessons[currentLessonIndex + 1].id : null;

  const isLessonCompleted = (id: string) => {
    return progress?.find(p => p.lessonId === id)?.completed;
  };

  const isModuleCompleted = (moduleId: string) => {
    const module = (modules as any[])?.find(m => m.id === moduleId);
    if (!module || !module.lessons || module.lessons.length === 0) return false;
    const fallback = user?.level || "Beginner";
    const targetLevel = moduleLevels[moduleId] || fallback;
    const filtered = (module.lessons as any[]).filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(targetLevel));
    const lessons = filtered.length > 0 ? filtered : (module.lessons as any[]);
    return lessons.every(l => isLessonCompleted(l.id));
  };

  const isModuleLocked = (moduleId: string) => {
    const module = (modules as any[])?.find(m => m.id === moduleId);
    if (!module || module.order === 1) return false;
    const previousModule = (modules as any[])?.find(m => m.order === module.order - 1);
    return previousModule ? !isModuleCompleted(previousModule.id) : false;
  };

  const isLessonLocked = (id: string) => {
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

  // Scroll progress state
  const [scrollProgress, setScrollProgress] = useState(0);

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    const progress = (target.scrollTop / (target.scrollHeight - target.clientHeight)) * 100;
    setScrollProgress(progress);
  };

  // Initialize code when lesson loads to challenge starter code or empty as fallback
  useEffect(() => {
    if (lesson?.challenges?.[0]) {
      setCode(lesson.challenges[0].initial_code || "");
    }
  }, [lesson]);

  const [quizResults, setQuizResults] = useState<Record<string, { selected: number; correct: boolean }>>({});

  const handleRun = async () => {
    if (!lesson?.challenges?.[0]) return;
    
    // Check if code is empty or just whitespace
    if (!code.trim()) {
      setError("Please write some code before running.");
      return;
    }
    
    // Check for input() calls
    const inputCount = getInputCount(code);
    
    if (inputCount > 0) {
      // Interactive mode: collect inputs one by one
      const calls = parseInputCalls(code);
      setInputCalls(calls);
      setTotalInputsNeeded(inputCount);
      setCollectedInputs([]);
      setCurrentInputIndex(0);
      setInteractiveOutput("");
      setError(null);
      setOutput("");
      setIsInteractiveMode(true);
      setIsWaitingForInput(true);
    } else {
      // Non-interactive: just run the code
      setIsInteractiveMode(false);
      setOutput("Running...");
      setError(null);
      
      try {
        const result = await runMutation.mutateAsync({
          id: lesson.challenges[0].id,
          code: code.trim(),
          input: ""
        });
        
        setOutput(result.output || "");
        
        if (result.error) {
          setError(result.error);
        } else if ((result as any).passed || !result.error) {
          confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
          });
          
          // Determine the message based on current progress
          const currentProgress = progress?.find(p => p.lessonId === lessonId);
          const quizDone = currentProgress?.quizCompleted;
          
          toast({
            title: "Coding Challenge Completed! ✅",
            description: quizDone 
              ? "Challenge passed! Next lesson unlocked ✅" 
              : "Coding challenge completed successfully!",
            className: "bg-green-500 text-white border-none",
          });
          
          setMasteryImpact(0.06);
          setIsCompleted(true);
          
          if (user) {
            // Refetch faster by only invalidating what's needed
            queryClient.invalidateQueries({ queryKey: ["/api/user-progress"] });
            refetch();
          }
        } else {
          setError(result.error || "Code ran but didn't pass all test cases. Check your output above.");
        }
      } catch (err: any) {
        console.error("Run challenge error:", err);
        setError(err.message || "Failed to execute code");
        setOutput("");
      }
    }
  };

  const handleInteractiveInput = async (value: string) => {
    const newInputs = [...collectedInputs, value];
    setCollectedInputs(newInputs);

    const inputCall = inputCalls[currentInputIndex];
    const prompt = inputCall?.prompt || "Input";
    const displayOutput = interactiveOutput + prompt + "\n" + value + "\n";
    setInteractiveOutput(displayOutput);

    if (newInputs.length < totalInputsNeeded) {
      setCurrentInputIndex(newInputs.length);
      setIsWaitingForInput(true);
      return;
    }

    setIsWaitingForInput(false);
    setOutput("Running...");
    setError(null);

    try {
      const result = await runMutation.mutateAsync({
        id: lesson?.challenges?.[0].id as string,
        code: code.trim(),
        input: newInputs.join("\n"),
      });

      // Remove repeated prompt echoes from backend stdout
      const cleanedRuntimeOutput = stripInputPromptsFromOutput(
        result.output || "",
        inputCalls.map((c) => c.prompt || "")
      );

      const finalOutput = formatInteractiveOutput(
        inputCalls.map((c) => c.prompt || ""),
        newInputs,
        cleanedRuntimeOutput
      );

      setInteractiveOutput(finalOutput);
      setOutput(finalOutput);

      if (result.error) {
        setError(result.error);
      } else if ((result as any).passed) {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 },
        });

        const currentProgress = progress?.find(p => p.lessonId === lessonId);
        const quizDone = currentProgress?.quizCompleted;

        toast({
          title: "Coding Challenge Completed! ✅",
          description: quizDone 
            ? "Challenge passed! Next lesson unlocked ✅" 
            : "Coding challenge completed successfully!",
          className: "bg-green-500 text-white border-none",
        });
        setMasteryImpact(0.06);
        setIsCompleted(true);

        if (user) {
          try {
            await progressMutation.mutateAsync({
              userId: String(user.id),
              lessonId,
              completed: false, // Will be set to true by backend only when both quiz and challenge are done
              lastCode: code,
              score: 100,
              challengeCompleted: true,
              completedAt: new Date().toISOString(),
            });
            
            queryClient.invalidateQueries({ queryKey: ["/api/user-progress"] });
            refetch();
          } catch (err) {
            console.error("Error updating progress after challenge:", err);
          }
        }

        setOutput((prev) => (prev ? prev + "\n\n" : "") + "✅ All tests passed!");
      } else {
        setError(result.error || "Code ran but didn't pass all test cases. Check your output above.");
      }
    } catch (err: any) {
      console.error("Run challenge error:", err);
      setError(err.message || "Failed to execute code");
      setOutput("");
    } finally {
      setIsInteractiveMode(false);
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
      title = "Lesson Locked";
      description = lessonErrorMessage || "Complete the required lessons to unlock this one.";
      if (description.toLowerCase().includes("placement")) {
          action = (
            <button
              onClick={() => (window.location.href = "/placement-quiz")}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
            >
              Take the placement quiz
            </button>
          );
      } else {
          action = (
            <button
              onClick={() => (window.location.href = "/curriculum")}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
            >
              Back to Curriculum
            </button>
          );
      }
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
                 <Button
                  size="lg"
                  className="rounded-full px-8 h-14 text-lg font-semibold gap-2 shadow-lg shadow-primary/20"
                  onClick={() => {
                    const completed = isLessonCompleted(lessonId);
                    if (!completed) {
                      const currentProgress = progress?.find(p => p.lessonId === lessonId);
                      const quizDone = currentProgress?.quizCompleted ? true : false;
                      const challengeDone = currentProgress?.challengeCompleted ? true : false;
                      
                      let message = "";
                      if (!quizDone && !challengeDone) {
                        message = "Please complete both the Knowledge Check and the Coding Challenge to unlock the next lesson.";
                      } else if (!quizDone) {
                        message = "Please complete the Knowledge Check to unlock the next lesson.";
                      } else if (!challengeDone) {
                        message = "Please complete the Coding Challenge to unlock the next lesson.";
                      }
                      
                      toast({
                        title: "Mastery Required",
                        description: message || "Please complete all requirements to unlock the next lesson.",
                        variant: "default",
                      });
                      return;
                    }
                    
                    const nextId = (lesson as any).nextLessonId;
                    if (nextId) {
                      setLocation(`/lesson/${nextId}`);
                    } else {
                      setLocation('/curriculum');
                    }
                  }}
                >
                  Next Lesson
                  <ArrowRight className="w-5 h-5" />
                </Button>
             )}
           </div>
           {/* Progress Indicator */}
           <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted/50 px-3 py-1.5 rounded-full">
             <span>Track: {lesson.difficulty === "Advanced" ? "Pro" : lesson.difficulty}</span>
           </div>
        </div>
      </header>

      {/* Main Content Split */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Pane: Content */}
        <div 
          className="w-1/2 border-r border-border bg-card/30 overflow-y-auto p-8 scrollbar-thin relative"
          onScroll={handleScroll}
        >
          {/* Scroll Progress Bar */}
          <div className="absolute top-0 left-0 w-full h-1 z-10 bg-muted/20">
            <div 
              className="h-full bg-primary transition-all duration-150" 
              style={{ width: `${scrollProgress}%` }}
            />
          </div>

          <div className="max-w-2xl mx-auto markdown-content">
            <div className="mb-10 p-6 rounded-2xl border border-border bg-card shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <div className="text-sm font-medium text-muted-foreground mb-1 uppercase tracking-wider">Your Mastery</div>
                  <div className="text-3xl font-bold text-primary">{Math.round(masteryScore * 100)}%</div>
                </div>
                <div className="p-3 bg-primary/10 rounded-xl">
                  <Target className="w-6 h-6 text-primary" />
                </div>
              </div>
              <div className="text-sm text-muted-foreground mt-4 italic">"{encouragement}"</div>
            </div>
             
             <ReactMarkdown>
               {lesson.content.split(/🧪 Knowledge Check|❓ Knowledge Check|Knowledge Check/i)[0]}
             </ReactMarkdown>
            
            {(lesson as any)?.quizzes?.length > 0 && (
              <div className="mt-16 p-8 border border-border rounded-3xl bg-card/50 shadow-sm backdrop-blur-sm">
                <div className="flex items-center justify-between mb-8">
                  <div>
                    <h3 className="text-2xl font-bold tracking-tight mb-1">Knowledge Check</h3>
                    <p className="text-sm text-muted-foreground">Test your understanding of the concepts above.</p>
                  </div>
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <Bot className="w-5 h-5 text-primary" />
                  </div>
                </div>
                <QuizView
                  questions={(lesson as any).quizzes?.[0]?.questions || []}
                  onSubmit={async (answers) => {
                    try {
                      const questions = (lesson as any).quizzes?.[0]?.questions || [];
                      const correctCount = questions.reduce((acc: number, q: any) => {
                        const selectedIdx = answers[q.id];
                        const isCorrect = q.options?.[selectedIdx]?.correct;
                        return isCorrect ? acc + 1 : acc;
                      }, 0);
                      const score = Math.round((correctCount / questions.length) * 100);
                      
                      await progressMutation.mutateAsync({
                        lessonId: lessonId,
                        completed: false, // Will be set to true by backend only when both quiz and challenge are done
                        score: score,
                        quizCompleted: true,
                        lastCode: JSON.stringify(answers)
                      });
                      
                      // Refetch and show message
                      queryClient.invalidateQueries({ queryKey: ["/api/user-progress"] });
                      await refetch();
                      
                      // Get updated progress to check if challenge is also done
                      const updatedProgress = queryClient.getQueryData<any[]>(["/api/user-progress"])
                        ?.find(p => p.lessonId === lessonId);
                      const challengeDone = updatedProgress?.challengeCompleted;

                      const motivationalMessage = challengeDone
                        ? "Choice well made! Next lesson unlocked ✅"
                        : "Knowledge check completed successfully!";
                      
                      toast({
                        title: "Knowledge Check Completed! ✅",
                        description: motivationalMessage,
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
               <div className="mt-16 p-8 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent border border-primary/20 rounded-3xl relative overflow-hidden group">
                 <div className="absolute -top-4 -right-4 p-8 opacity-5 group-hover:opacity-10 transition-all duration-500 rotate-12">
                   <Code2 className="w-32 h-32" />
                 </div>
                 <h3 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
                   <Sparkles className="w-6 h-6" /> Coding Challenge
                 </h3>
                 <div className="markdown-content">
                   <ReactMarkdown>{lesson.challenges[0].description}</ReactMarkdown>
                 </div>
                 <div className="mt-6 flex items-center gap-2 text-sm text-primary font-medium">
                   <ChevronRight className="w-4 h-4" /> Use the editor on the right to solve
                 </div>
               </div>
             )}

             {isLessonCompleted(lessonId) && (
               <div className="mt-16 p-8 bg-primary/5 border border-primary/20 rounded-3xl text-center space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
                 <div className="inline-flex p-4 bg-primary/10 rounded-full">
                    <Sparkles className="w-8 h-8 text-primary" />
                 </div>
                 <div>
                    <h3 className="text-2xl font-bold">Lesson Mastered!</h3>
                    <p className="text-muted-foreground mt-2">You've successfully completed all requirements for this lesson.</p>
                 </div>
               </div>
             )}
          </div>
        </div>

        {/* Right Pane: Code Editor */}
        <div className="w-1/2 p-8 overflow-y-auto space-y-4 bg-background">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Interactive Runner</h2>
            <div className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded">main.py</div>
          </div>
          
          <div className="h-80 rounded-lg overflow-hidden border border-border bg-[#1e1e1e]">
            <Editor 
              code={code} 
              onChange={setCode}
            />
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={handleRun}
              disabled={runMutation.isPending}
              className="px-4 py-2 bg-primary text-primary-foreground font-medium rounded-lg disabled:opacity-50 flex items-center gap-2"
            >
              {runMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current" />}
              {runMutation.isPending ? "Running..." : "Run Code"}
            </button>
            <button
              onClick={() => setCode(lesson.challenges?.[0]?.initial_code || "")}
              className="px-4 py-2 border border-border rounded-lg text-sm hover:bg-muted font-medium flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" /> Reset
            </button>
          </div>

          {isInteractiveMode ? (
            <div className="h-64 rounded-lg overflow-hidden border border-border">
              <InteractiveConsole 
                isWaitingForInput={isWaitingForInput}
                onInputSubmit={handleInteractiveInput}
                output={interactiveOutput}
                error={error || undefined}
                isRunning={runMutation.isPending}
                prompts={inputCalls.map((c) => c.prompt || "")}
                currentPromptIndex={currentInputIndex}
              />
            </div>
          ) : (
            <div className="p-4 rounded-lg border border-border bg-[#0f0f0f] shadow-inner min-h-48 flex flex-col">
              <div className="text-sm font-medium mb-1 text-white flex items-center justify-between">
                <span>Console Output</span>
                {runMutation.isPending && <span className="text-yellow-500 animate-pulse text-xs">Running...</span>}
              </div>
              <div className="text-xs text-gray-500 mb-3 border-b border-[#333] pb-2">{getConsoleHelpText(code)}</div>
              
              <div className="font-mono text-sm whitespace-pre-wrap flex-1 overflow-auto">
                {output ? (
                  formatConsoleOutput(output).lines.map((line, idx) => (
                    <div key={idx} className={line.className}>
                      {line.text || '\u00A0'}
                    </div>
                  ))
                ) : (
                  <span className="text-gray-600 italic">Click "Run Code" to see the output here...</span>
                )}
                {error && (
                  <div className="mt-3 text-red-400 bg-red-400/10 p-2 rounded flex items-start gap-2">
                    <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                    <div>{error}</div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      <Suspense fallback={null}>
        <ChatTutor lessonId={lessonId} lessonTitle={lesson.title} lessonContent={lesson.content} />
      </Suspense>
    </div>
  );
}

import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useModules } from "@/hooks/use-modules";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/hooks/use-auth";
import { useMemo, useState, useEffect, useRef } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { Link, useLocation } from "wouter";
import { Loader2 } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

type QuizOption = {
  text: string;
  correct?: boolean;
};

export default function PlacementQuiz() {
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const hasTakenQuiz = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);
  const { data: modules, isLoading: loadingModules } = useModules({ enabled: hasTakenQuiz });
  const [phase, setPhase] = useState<"intro" | "active" | "resume">("intro");
  const [submitConfirm, setSubmitConfirm] = useState(false);
  const [exitConfirm, setExitConfirm] = useState(false);
  const firstLessonId = useMemo(() => {
    const lessons = modules?.flatMap((m: any) => (m.lessons || []).map((l: any) => ({ ...l, moduleOrder: m.order }))) || [];
    lessons.sort((a: any, b: any) => {
      if (a.moduleOrder !== b.moduleOrder) return a.moduleOrder - b.moduleOrder;
      return (a.order || 0) - (b.order || 0);
    });
    return lessons[0]?.id || null;
  }, [modules]);

  const { data: diagnostic, isLoading: loadingAttempts } = useQuery({
    queryKey: ["/api/diagnostic"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/diagnostic/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return null;
      if (!res.ok) throw new Error("Failed to fetch quiz attempts");
      return res.json();
    },
    enabled: !!user,
  });

  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(900);
  const [expired, setExpired] = useState(false);
  const [violationCount, setViolationCount] = useState(0);
  const [tabWarning, setTabWarning] = useState(false);
  const [violationDialog, setViolationDialog] = useState(false);
  const [warningMessage, setWarningMessage] = useState<string>("");
  const [attemptId, setAttemptId] = useState<string | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const lastViolationTsRef = useMemo(() => ({ ts: 0 }), []);
  const isSubmittingRef = useRef(false);
  const hasSubmittedRef = useRef(false);
  const [hasStartedAnswering, setHasStartedAnswering] = useState(false);
  const phaseRef = useRef<"intro" | "active" | "resume">("intro");

  useEffect(() => {
    const bootstrap = async () => {
      try {
        const meta = diagnostic?.attemptMeta;
        if (meta?.attemptId) {
          setAttemptId(String(meta.attemptId));
        }
        if (meta?.startTime && meta?.durationSeconds) {
          const startMillis = new Date(meta.startTime).getTime();
          const deadline = startMillis + (meta.durationSeconds * 1000);
          const now = Date.now();
          const remaining = Math.max(Math.floor((deadline - now) / 1000), 0);
          setTimeLeft(remaining);
          if (remaining === 0) {
            setExpired(true);
          }
          if (!meta.completedAt && meta.status === "IN_PROGRESS" && remaining > 0) {
            setPhase("resume");
          }
        }
      } catch {}
    };
    bootstrap();
  }, [diagnostic]);

  // Keep phaseRef in sync so timer effect can read current phase without re-registering
  useEffect(() => {
    phaseRef.current = phase;
  }, [phase]);

  // Only tick the clock when the quiz is active
  useEffect(() => {
    if (phase !== "active") return;
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          setExpired(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [phase]);

  useEffect(() => {
    const registerViolation = () => {
      const now = Date.now();
      if (now - lastViolationTsRef.ts < 1500) return;
      lastViolationTsRef.ts = now;
      setViolationCount((prev) => {
        const next = prev + 1;
        if (next === 1) {
          setWarningMessage("You switched tabs. Please stay on the test page.");
          setTabWarning(true);
        } else if (next === 2) {
          setWarningMessage("Final warning: One more tab switch will submit your test.");
          setTabWarning(true);
        }
        return next;
      });
    };
    const onVisibility = () => {
      // Small delay to prevent accidental triggers from background popups/notifications
      setTimeout(() => {
        if (document.hidden) {
          registerViolation();
        }
      }, 300);
    };
    const onBlur = () => {
       // Only register blur if tab isn't already hidden (to avoid double counting)
       if (!document.hidden) {
         registerViolation();
       }
    };
    const onContext = (e: Event) => {
      // Allow right-click but maybe warn? Many people use it for translation etc.
      // e.preventDefault(); 
    };
    const onKey = (e: KeyboardEvent) => {
      const key = e.key.toLowerCase();
      const ctrl = e.ctrlKey || e.metaKey;
      if (ctrl && (key === "c" || key === "v")) {
        // e.preventDefault(); // Might be too restrictive for some setups
      }
      if (key === "f12" || (ctrl && key === "shift")) {
        e.preventDefault();
      }
    };
    document.addEventListener("visibilitychange", onVisibility);
    window.addEventListener("blur", onBlur);
    document.addEventListener("contextmenu", onContext);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("blur", onBlur);
      document.removeEventListener("contextmenu", onContext);
      document.removeEventListener("keydown", onKey);
    };
  }, []);

  useEffect(() => {
    const VIOLATION_LIMIT = 5;
    // Never auto-submit if user hasn't started answering — prevents blank quiz from firing
    if (!hasStartedAnswering) return;
    if (violationCount >= VIOLATION_LIMIT && !expired) {
      setExpired(true);
      if (attemptId && !hasSubmittedRef.current) {
        handleSubmit(true);
      }
    } else if (expired) {
      if (attemptId && !hasSubmittedRef.current && !isSubmittingRef.current) {
        handleSubmit(true);
      }
    }
  }, [violationCount, expired, attemptId, hasStartedAnswering]);

  // No onboarding modal; banner handled on Dashboard

  const placementCompleted = hasTakenQuiz;
  const quiz = diagnostic?.quiz;
  const questions = diagnostic?.questions || [];

  const handleSelect = (questionId: string, optionIndex: number) => {
    if (expired) return;
    setHasStartedAnswering(true);
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  };

  const handleSubmit = async (auto?: boolean) => {
    if (hasSubmittedRef.current || isSubmittingRef.current) return;
    setError(null);
    if (!quiz || questions.length === 0) {
      setError("No placement quiz is available right now.");
      return;
    }
    if (auto && !attemptId) {
      // Attempt not registered yet; wait briefly and retry once
      setTimeout(() => handleSubmit(true), 400);
      return;
    }

    if (!auto) {
      const unanswered = questions.some((q: any) => answers[q.id] === undefined);
      if (unanswered) {
        setError("Answer all questions before submitting.");
        return;
      }
    }

    try {
      isSubmittingRef.current = true;
      setSubmitting(true);
      const accessToken = getAccessToken();
      if (!accessToken) {
        console.warn("No access token found for diagnostic submission");
      }
      const res = await fetch(apiUrl("/diagnostic/submit/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({
          quizId: quiz.id,
          answers: questions.map((q: any) => {
            const tempOpts = Array.isArray(q.options) ? q.options : [];
            const selectedOpt = answers[q.id] !== undefined ? tempOpts[answers[q.id]] : null;
            return {
              questionId: q.id,
              selectedIndex: answers[q.id] !== undefined ? answers[q.id] : -1,
              selectedOptionId: selectedOpt?.id ?? null,
            };
          }),
          violationCount,
        }),
        credentials: "include",
      });
      if (!res.ok) {
        if (res.status === 409) {
          // Conflict usually means attempt already submitted or locked
          await queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
          setLocation("/dashboard");
          return;
        }
        throw new Error("Failed to submit diagnostic quiz");
      }
      const data = await res.json();
      await queryClient.invalidateQueries({ queryKey: ["/api/metrics"] });
      await queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
      await queryClient.invalidateQueries({ queryKey: ["/api/modules"] });
      await queryClient.invalidateQueries({ queryKey: ["/api/recommendations"] });
      await queryClient.invalidateQueries({ queryKey: ["/api/recommend-next"] });
      await queryClient.invalidateQueries({ queryKey: ["/api/analytics"] });
      
      if (violationCount >= 3) {
        hasSubmittedRef.current = true;
        setViolationDialog(true);
        setExpired(true);
      } else {
        hasSubmittedRef.current = true;
        toast({
          title: data?.timeUp ? "Time is up. Your quiz has been submitted." : "Placement quiz completed",
          description: `Score: ${Math.round((data?.weightedScore || data?.overallScore || 0) * 100)}%`,
        });
        setExpired(true);
        // Ensure user + modules are refetched so subsequent pages pick the correct track immediately
        queryClient.removeQueries({ queryKey: ["/api/modules"] }); // CLEAR cache completely
        queryClient.removeQueries({ queryKey: ["/api/auth/user"] }); // CLEAR user cache
        
        // Fetch fresh data directly
        const accessToken = getAccessToken();
        const [userRes, modulesRes] = await Promise.all([
          fetch(apiUrl("/auth/user"), { headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {}, credentials: "include" }),
          fetch(apiUrl("/api/modules/"), { headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : {}, credentials: "include" }),
        ]);
        
        const freshUser = userRes.ok ? await userRes.json() : null;
        const freshModules = modulesRes.ok ? await modulesRes.json() : [];
        
        // Update cache with fresh data for when user navigates manually
        queryClient.setQueryData(["/api/auth/user"], freshUser);
        queryClient.setQueryData(["/api/modules"], freshModules);
        
        // User will click "Go to first lesson" button manually - no auto-redirect
      }
    } catch (err: any) {
      setError(err.message || "Failed to submit diagnostic quiz");
    } finally {
      isSubmittingRef.current = false;
      setSubmitting(false);
    }
  };

  const startTest = async () => {
    setError(null);
    try {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/diagnostic/start/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        credentials: "include",
      });
      const data = await res.json().catch(() => ({}));
      const meta = data?.attemptMeta;
      if (meta?.attemptId) setAttemptId(String(meta.attemptId));
      if (meta?.startTime && meta?.durationSeconds) {
        const startMillis = new Date(meta.startTime).getTime();
        const deadline = startMillis + (meta.durationSeconds * 1000);
        const now = Date.now();
        setTimeLeft(Math.max(Math.floor((deadline - now) / 1000), 0));
      }
      setPhase("active");
    } catch (e: any) {
      setError(e?.message || "Failed to start test");
    }
  };

  const cancelAttempt = async () => {
    try {
      const accessToken = getAccessToken();
      await fetch(apiUrl("/diagnostic/cancel/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        credentials: "include",
      });
    } catch {}
    setLocation("/dashboard");
  };

  if (loadingAttempts || (hasTakenQuiz && loadingModules)) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full py-20">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  if (placementCompleted && !firstLessonId) {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center">
          <h1 className="text-2xl font-bold">No lessons found</h1>
          <p className="text-muted-foreground mt-2">Add lessons to enable the placement quiz.</p>
        </div>
      </Layout>
    );
  }

  if (placementCompleted) {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center space-y-4">
          <h1 className="text-2xl font-bold">Placement quiz completed</h1>
          <p className="text-muted-foreground">You can start learning now.</p>
          <Link href={`/lesson/${firstLessonId}`}>
            <Button>Go to first lesson</Button>
          </Link>
        </div>
      </Layout>
    );
  }

  if (phase === "intro") {
    return (
      <Layout>
        <div className="max-w-2xl mx-auto py-12 px-4 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Placement Test Instructions</CardTitle>
              <CardDescription>Read these rules before starting.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <ol className="list-decimal pl-5 space-y-2">
                <li>This test determines your Python skill level.</li>
                <li>Please answer questions honestly.</li>
                <li>Avoid refreshing the page during the test.</li>
                <li>Avoid switching browser tabs during the test.</li>
                <li>Your learning path will be generated based on your performance.</li>
                <li>If you exit before completing, the test will restart.</li>
              </ol>
              <div className="flex gap-3 pt-4">
                <Button onClick={startTest}>Start Test</Button>
                <Button variant="outline" onClick={() => setLocation("/dashboard")}>Go Back</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </Layout>
    );
  }

  if (phase === "resume") {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4">
          <Card>
            <CardHeader>
              <CardTitle>Unfinished Placement Test</CardTitle>
              <CardDescription>You have an unfinished placement test.</CardDescription>
            </CardHeader>
            <CardContent className="flex gap-3">
              <Button onClick={() => setPhase("active")}>Resume Test</Button>
              <Button variant="outline" onClick={cancelAttempt}>Cancel Attempt</Button>
            </CardContent>
          </Card>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto py-12 px-4 space-y-6">
        <AlertDialog open={tabWarning} onOpenChange={setTabWarning}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Academic Integrity</AlertDialogTitle>
              <AlertDialogDescription>
                {warningMessage || "Warning: Leaving the quiz tab is not allowed. Repeated violations will automatically submit your quiz."}
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogAction>Continue</AlertDialogAction>
          </AlertDialogContent>
        </AlertDialog>
        <AlertDialog open={violationDialog} onOpenChange={setViolationDialog}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle className="text-destructive flex items-center gap-2">
                Quiz Terminated
              </AlertDialogTitle>
              <AlertDialogDescription className="text-foreground font-medium">
                Your placement quiz has been automatically submitted due to repeated tab-switching violations. 
                <br /><br />
                You will need to reattempt the quiz from the dashboard to unlock your personalized learning path.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogAction onClick={() => setLocation("/dashboard")}>
              Go to Dashboard
            </AlertDialogAction>
          </AlertDialogContent>
        </AlertDialog>
        <AlertDialog open={submitConfirm} onOpenChange={setSubmitConfirm}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Submit Test</AlertDialogTitle>
              <AlertDialogDescription>
                Are you sure you want to submit your answers?
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogCancel>Review Again</AlertDialogCancel>
            <AlertDialogAction onClick={() => handleSubmit()}>Submit</AlertDialogAction>
          </AlertDialogContent>
        </AlertDialog>
        <AlertDialog open={exitConfirm} onOpenChange={setExitConfirm}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Exit Test</AlertDialogTitle>
              <AlertDialogDescription>
                Are you sure you want to exit the placement test? Your progress will not be saved.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogCancel>Continue Test</AlertDialogCancel>
            <AlertDialogAction onClick={cancelAttempt}>Exit Test</AlertDialogAction>
          </AlertDialogContent>
        </AlertDialog>
        <Card>
          <CardHeader>
            <CardTitle>Placement Quiz</CardTitle>
            <CardDescription>Answer a few questions to personalize your learning path.</CardDescription>
            {!placementCompleted && (
              <div className="text-xs text-muted-foreground mt-2">
                You need to complete the placement quiz to personalize your learning path.
              </div>
            )}
            <div className="flex items-center justify-between text-xs text-muted-foreground mt-2">
              <span>Time left: {Math.floor(timeLeft / 60)}:{String(timeLeft % 60).padStart(2, "0")}</span>
              <span className={cn(violationCount > 0 ? "text-orange-500 font-medium" : "")}>
                Violations: {violationCount} / 5
              </span>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {questions.length === 0 ? (
              <div className="text-muted-foreground">No placement quiz is available right now.</div>
            ) : (
              <div className="space-y-6">
                {questions.map((q: any, index: number) => (
                  <div key={q.id} className="space-y-3">
                    <div className="font-medium">
                      {index + 1}. {q.text}
                    </div>
                    <div className="grid gap-2">
                      {(Array.isArray(q.options) ? q.options : []).map((opt: QuizOption, optIndex: number) => (
                        <label key={`${q.id}-${optIndex}`} className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:border-primary/60">
                          <input
                            type="radio"
                            name={`question-${q.id}`}
                            checked={answers[q.id] === optIndex}
                            onChange={() => handleSelect(q.id, optIndex)}
                            disabled={expired}
                          />
                          <span>{opt.text}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {error && <div className="text-sm text-destructive">{error}</div>}

            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setExitConfirm(true)} disabled={submitting || expired}>
                Exit Test
              </Button>
              <Button onClick={() => setSubmitConfirm(true)} disabled={submitting || questions.length === 0 || expired}>
                {submitting ? "Submitting..." : "Submit quiz"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

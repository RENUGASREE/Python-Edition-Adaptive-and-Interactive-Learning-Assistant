import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useModules } from "@/hooks/use-modules";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/hooks/use-auth";
import { useMemo, useState, useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { Link, useLocation } from "wouter";
import { Loader2 } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
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
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/diagnostic"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return null;
      if (!res.ok) throw new Error("Failed to fetch quiz attempts");
      return res.json();
    },
  });

  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(900);
  const [expired, setExpired] = useState(false);
  const [violationCount, setViolationCount] = useState(0);
  const [tabWarning, setTabWarning] = useState(false);
  const [warningMessage, setWarningMessage] = useState<string>("");
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const lastViolationTsRef = useMemo(() => ({ ts: 0 }), []);

  useEffect(() => {
    const startAttempt = async () => {
      try {
        const accessToken = localStorage.getItem("access_token");
        const res = await fetch(apiUrl("/diagnostic/start"), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
          },
          credentials: "include",
        });
        const data = await res.json().catch(() => ({}));
        const meta = data?.attemptMeta || diagnostic?.attemptMeta;
        if (meta?.attemptId) {
          setAttemptId(Number(meta.attemptId));
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
        }
      } catch {}
    };
    startAttempt();
  }, [diagnostic]);

  useEffect(() => {
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
  }, []);

  useEffect(() => {
    const registerViolation = () => {
      const now = Date.now();
      if (now - lastViolationTsRef.ts < 1500) return;
      lastViolationTsRef.ts = now;
      setViolationCount((prev) => {
        const next = prev + 1;
        if (next === 1) {
          setWarningMessage("Warning: Leaving the quiz tab is not allowed. Repeated violations will automatically submit your quiz.");
          setTabWarning(true);
        } else if (next === 2) {
          setWarningMessage("Final Warning: Switching tabs again will submit your quiz.");
          setTabWarning(true);
        }
        return next;
      });
    };
    const onVisibility = () => {
      if (document.hidden) {
        registerViolation();
      }
    };
    const onBlur = () => {
      registerViolation();
    };
    const onContext = (e: Event) => {
      e.preventDefault();
    };
    const onKey = (e: KeyboardEvent) => {
      const key = e.key.toLowerCase();
      const ctrl = e.ctrlKey || e.metaKey;
      if (ctrl && (key === "c" || key === "v")) {
        e.preventDefault();
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
    if (violationCount >= 3 && !expired) {
      setExpired(true);
      if (attemptId) {
        handleSubmit(true);
      }
    } else if (expired) {
      if (attemptId) {
        handleSubmit(true);
      }
    }
  }, [violationCount, expired, attemptId]);

  // No onboarding modal; banner handled on Dashboard

  const placementCompleted = hasTakenQuiz;
  const quiz = diagnostic?.quiz;
  const questions = diagnostic?.questions || [];

  const handleSelect = (questionId: number, optionIndex: number) => {
    if (expired) return;
    setAnswers((prev) => ({ ...prev, [questionId]: optionIndex }));
  };

  const handleSubmit = async (auto?: boolean) => {
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
      setSubmitting(true);
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/diagnostic/submit"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({
          quizId: quiz.id,
          answers: questions.map((q: any) => ({
            questionId: q.id,
            selectedIndex: answers[q.id],
          })),
          violationCount,
        }),
        credentials: "include",
      });
      if (!res.ok) {
        throw new Error("Failed to submit diagnostic quiz");
      }
      const data = await res.json();
      await queryClient.invalidateQueries({ queryKey: ["/api/metrics"] });
      await queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
      toast({
        title: data?.timeUp ? "Time is up. Your quiz has been submitted." : "Placement quiz completed",
        description: `Score: ${Math.round((data?.weightedScore || data?.overallScore || 0) * 100)}%`,
      });
      setExpired(true);
      setTimeout(() => setLocation("/dashboard"), 400);
    } catch (err: any) {
      setError(err.message || "Failed to submit diagnostic quiz");
    } finally {
      setSubmitting(false);
    }
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
        <Card>
          <CardHeader>
            <CardTitle>Placement Quiz</CardTitle>
            <CardDescription>Answer a few questions to personalize your learning path.</CardDescription>
            {!placementCompleted && (
              <div className="text-xs text-muted-foreground mt-2">
                You need to complete the placement quiz to personalize your learning path.
              </div>
            )}
            <div className="text-xs text-muted-foreground mt-2">
              Time left: {Math.floor(timeLeft / 60)}:{String(timeLeft % 60).padStart(2, "0")}
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

            <div className="flex justify-end">
              <Button onClick={() => handleSubmit()} disabled={submitting || questions.length === 0 || expired}>
                {submitting ? "Submitting..." : "Submit quiz"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

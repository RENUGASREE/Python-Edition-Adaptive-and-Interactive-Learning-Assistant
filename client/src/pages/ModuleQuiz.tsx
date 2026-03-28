import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useModule } from "@/hooks/use-modules";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/hooks/use-auth";
import { useMemo, useState, useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { Link, useLocation, useParams } from "wouter";
import { Loader2 } from "lucide-react";
import QuizView from "@/components/QuizView";
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

export default function ModuleQuiz() {
  const { id } = useParams();
  const moduleId = id || "";
  const { data: module, isLoading: loadingModule } = useModule(moduleId);
  const { user } = useAuth();
  const { data: quizAttempts, isLoading: loadingAttempts, refetch } = useQuery({
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

  const moduleLevel = useMemo(() => {
    const fallback = user?.level || "Beginner";
    const match = (quizAttempts || [])
      .map((attempt: any) => parseModuleLevel(attempt?.notes))
      .find((parsed: { moduleId: string; level: string } | null) => parsed?.moduleId === moduleId);
    return match?.level || fallback;
  }, [quizAttempts, moduleId, user?.level]);

  const moduleLessons = useMemo(() => {
    const lessons = (module as any)?.lessons || [];
    const filtered = lessons.filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(moduleLevel));
    return (filtered.length > 0 ? filtered : lessons).sort((a: any, b: any) => (a.order || 0) - (b.order || 0));
  }, [module, moduleLevel]);

  const { data: moduleQuizData, isLoading: loadingQuiz } = useQuery({
    queryKey: ["/api/modules", moduleId, "quiz"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(`/modules/${moduleId}/quiz/`), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch module quiz content");
      return res.json();
    },
    enabled: !!moduleId && !!module,
  });

  const effectiveQuestions = useMemo(() => {
    return moduleQuizData?.questions || [];
  }, [moduleQuizData]);

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(900);
  const [tabWarning, setTabWarning] = useState(false);
  const [masteryImpact, setMasteryImpact] = useState<number | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [, setLocation] = useLocation();

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const handler = () => {
      if (document.hidden) {
        setTabWarning(true);
      }
    };
    document.addEventListener("visibilitychange", handler);
    return () => document.removeEventListener("visibilitychange", handler);
  }, []);

  const moduleQuizCompleted = (quizAttempts || []).some((attempt: any) => attempt?.notes?.includes(`module:${moduleId}:level:`));

  const handleSubmit = async (quizAnswers: Record<string, number>) => {
    setError(null);
    if (effectiveQuestions.length === 0) {
      setError("No module quiz is available right now.");
      return;
    }

    const unanswered = effectiveQuestions.some((q: any) => quizAnswers[q.id] === undefined);
    if (unanswered) {
      setError("Answer all questions before submitting.");
      return;
    }

    const totalPoints = effectiveQuestions.reduce((sum: number, q: any) => sum + (q.points || 10), 0);
    const earnedPoints = effectiveQuestions.reduce((sum: number, q: any) => {
      const options: QuizOption[] = Array.isArray(q.options) ? q.options : [];
      const selectedIndex = quizAnswers[q.id];
      const selectedOption = options[selectedIndex];
      if (selectedOption?.correct) return sum + (q.points || 10);
      return sum;
    }, 0);

    const scorePercent = totalPoints > 0 ? Math.round((earnedPoints / totalPoints) * 100) : 0;
    const level = scorePercent >= 80 ? "Pro" : scorePercent >= 50 ? "Intermediate" : "Beginner";
    setMasteryImpact(scorePercent >= 80 ? 0.08 : scorePercent >= 50 ? 0.04 : 0.02);

    try {
      setSubmitting(true);
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/quiz-attempts/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ score: scorePercent, notes: `module:${moduleId}:level:${level}` }),
        credentials: "include",
      });
      if (!res.ok) {
        throw new Error("Failed to submit module quiz");
      }

      await queryClient.invalidateQueries({ queryKey: ["/api/quiz-attempts"] });
      await refetch();
      toast({
        title: "Module quiz completed",
        description: `Your module level is set to ${level}.`,
      });
      setLocation("/curriculum");
    } catch (err: any) {
      setError(err.message || "Failed to submit module quiz");
    } finally {
      setSubmitting(false);
    }
  };

  if (loadingModule || loadingAttempts || loadingQuiz) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full py-20">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  if (!moduleId || !module) {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center">
          <h1 className="text-2xl font-bold">Module not found</h1>
          <p className="text-muted-foreground mt-2">Choose a module from the curriculum.</p>
          <Link href="/curriculum">
            <Button className="mt-4">Go to curriculum</Button>
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
              <AlertDialogTitle>Stay focused</AlertDialogTitle>
              <AlertDialogDescription>
                Tab switching is discouraged during quizzes. Please stay on this page.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogAction>Continue</AlertDialogAction>
          </AlertDialogContent>
        </AlertDialog>
        <Card>
          <CardHeader>
            <CardTitle>{module.title} Quiz</CardTitle>
            <CardDescription>Answer the questions to personalize this module.</CardDescription>
            <div className="text-xs text-muted-foreground mt-2">
              Time left: {Math.floor(timeLeft / 60)}:{String(timeLeft % 60).padStart(2, "0")}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {effectiveQuestions.length === 0 ? (
              <div className="text-muted-foreground">No module quiz is available right now.</div>
            ) : (
              <QuizView questions={effectiveQuestions} onSubmit={handleSubmit} />
            )}

            {error && <div className="text-sm text-destructive">{error}</div>}
            {masteryImpact !== null && (
              <div className="text-sm text-muted-foreground">
                Estimated mastery impact: +{Math.round(masteryImpact * 100)}%
              </div>
            )}

            <div className="flex items-center justify-between">
              <Link href="/curriculum">
                <Button variant="outline">Back to curriculum</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

import { createContext, useContext } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useAuth } from "@/hooks/use-auth";

type Recommendation = {
  next_module: { id: number; title: string } | null;
  next_topic: string;
  difficulty_level: string;
  reason_for_recommendation: Record<string, number>;
  confidence_score: number;
  recommended_lesson_id?: number | null;
  recommended_lesson_title?: string | null;
  reasons?: string[];
  reason_codes?: string[];
};

type Analytics = {
  masteryProgression: Array<{ created_at: string; overall_score: number }>;
  interactionSeries?: Array<{ created_at: string; topic: string; correctness: boolean }>;
  learningGain: number;
  weakestTopic: string | null;
  strongestTopic: string | null;
  engagementIndex: number;
  riskScore: number;
};

type AdaptiveContextValue = {
  recommendation?: Recommendation;
  analytics?: Analytics;
  masteryVector?: Record<string, number>;
  isLoading: boolean;
};

const AdaptiveContext = createContext<AdaptiveContextValue>({
  isLoading: true,
});

export function AdaptiveProvider({ children }: { children: React.ReactNode }) {
  const { user, isAuthenticated } = useAuth();
  const hasCompletedQuiz = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);

  const { data: recommendation, isLoading: loadingRecommendation } = useQuery({
    queryKey: ["/api/recommend-next"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/recommend-next/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch recommendation");
      return res.json();
    },
    enabled: isAuthenticated && hasCompletedQuiz,
  });

  const { data: analytics, isLoading: loadingAnalytics } = useQuery({
    queryKey: ["/api/analytics"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/analytics/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch analytics");
      return res.json();
    },
    enabled: isAuthenticated && hasCompletedQuiz,
  });

  const { data: metrics, isLoading: loadingMetrics } = useQuery({
    queryKey: ["/api/metrics"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/metrics/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch metrics");
      return res.json();
    },
    enabled: isAuthenticated && hasCompletedQuiz,
  });

  return (
    <AdaptiveContext.Provider
      value={{
        recommendation,
        analytics,
        masteryVector: metrics?.masteryVector,
        isLoading: loadingRecommendation || loadingAnalytics || loadingMetrics,
      }}
    >
      {children}
    </AdaptiveContext.Provider>
  );
}

export function useAdaptiveContext() {
  return useContext(AdaptiveContext);
}

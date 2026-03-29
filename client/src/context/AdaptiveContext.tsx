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

  // Batch fetch all adaptive data in parallel for better performance
  const { data: adaptiveData, isLoading: loadingAdaptive } = useQuery({
    queryKey: ["/api/adaptive-data"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const headers = accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined;
      
      const [recommendationRes, analyticsRes, metricsRes] = await Promise.all([
        fetch(apiUrl("/recommend-next/"), { credentials: "include", headers }),
        fetch(apiUrl("/analytics/"), { credentials: "include", headers }),
        fetch(apiUrl("/metrics/"), { credentials: "include", headers }),
      ]);
      
      const [recommendation, analytics, metrics] = await Promise.all([
        recommendationRes.ok ? recommendationRes.json() : null,
        analyticsRes.ok ? analyticsRes.json() : null,
        metricsRes.ok ? metricsRes.json() : null,
      ]);
      
      return { recommendation, analytics, metrics };
    },
    enabled: isAuthenticated && hasCompletedQuiz,
    staleTime: 2 * 60 * 1000, // 2 minutes
  });

  return (
    <AdaptiveContext.Provider
      value={{
        recommendation: adaptiveData?.recommendation,
        analytics: adaptiveData?.analytics,
        masteryVector: adaptiveData?.metrics?.masteryVector,
        isLoading: loadingAdaptive,
      }}
    >
      {children}
    </AdaptiveContext.Provider>
  );
}

export function useAdaptiveContext() {
  return useContext(AdaptiveContext);
}

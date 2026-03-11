import { useAdaptiveContext } from "@/context/AdaptiveContext";


export function useRecommendation() {
  const { recommendation, isLoading } = useAdaptiveContext();
  return { recommendation, isLoading };
}

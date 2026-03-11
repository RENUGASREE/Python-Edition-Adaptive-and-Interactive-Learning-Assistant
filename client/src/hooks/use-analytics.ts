import { useAdaptiveContext } from "@/context/AdaptiveContext";


export function useAnalytics() {
  const { analytics, isLoading } = useAdaptiveContext();
  return { analytics, isLoading };
}

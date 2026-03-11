import { useAdaptiveContext } from "@/context/AdaptiveContext";


export function useMastery() {
  const { masteryVector, isLoading } = useAdaptiveContext();
  return { masteryVector, isLoading };
}

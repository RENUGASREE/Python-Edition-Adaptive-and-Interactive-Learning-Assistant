import { useQuery } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { refreshAndRetry } from "@/lib/api-auth";
import { useAuth } from "@/hooks/use-auth";
import { type Module, type Lesson } from "@/types";

type ModuleWithLessons = Module & { lessons: Lesson[] };

export function useModules(options?: { enabled?: boolean }) {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/modules"],
    queryFn: async () => {
      return refreshAndRetry<ModuleWithLessons[]>((token) =>
        fetch(apiUrl("/api/modules/"), {
          credentials: "include",
          headers: { Authorization: `Bearer ${token}` },
        })
      );
    },
    enabled: (options?.enabled ?? true) && isAuthenticated,
  });
}

export function useModule(id: string) {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/modules", id],
    queryFn: async () => {
      return refreshAndRetry<ModuleWithLessons>((token) =>
        fetch(apiUrl(`/api/modules/${id}/`), {
          credentials: "include",
          headers: { Authorization: `Bearer ${token}` },
        })
      );
    },
    enabled: !!id && isAuthenticated,
  });
}

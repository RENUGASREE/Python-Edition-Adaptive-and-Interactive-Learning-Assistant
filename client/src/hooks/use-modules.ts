import { useQuery } from "@tanstack/react-query";
import { api, buildUrl } from "@shared/routes";
import { apiUrl } from "@/lib/api";
import { type Module, type Lesson } from "@shared/schema";

type ModuleWithLessons = Module & { lessons: Lesson[] };

export function useModules(options?: { enabled?: boolean }) {
  return useQuery({
    queryKey: [api.modules.list.path],
    queryFn: async () => {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl(api.modules.list.path), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch modules");
      return api.modules.list.responses[200].parse(await res.json()) as ModuleWithLessons[];
    },
    enabled: options?.enabled ?? true,
  });
}

export function useModule(id: number) {
  return useQuery({
    queryKey: [api.modules.get.path, id],
    queryFn: async () => {
      const url = buildUrl(api.modules.get.path, { id });
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl(url), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch module");
      return api.modules.get.responses[200].parse(await res.json());
    },
    enabled: !!id,
  });
}

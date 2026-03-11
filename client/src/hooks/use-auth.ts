import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { User } from "@shared/models/auth";
import { apiUrl } from "@/lib/api";

async function fetchUser(): Promise<User | null> {
  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!accessToken) {
    return null;
  }

  const attemptFetch = async (token: string) => {
    const response = await fetch(apiUrl("/auth/user"), {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      credentials: "include",
    });
    return response;
  };

  let response = await attemptFetch(accessToken);
  if (response.status === 401 && refreshToken) {
    const refreshResponse = await fetch(apiUrl("/token/refresh/"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
      credentials: "include",
    });

    if (refreshResponse.ok) {
      const data = await refreshResponse.json();
      if (data?.access) {
        localStorage.setItem('access_token', data.access);
        response = await attemptFetch(data.access);
      }
    } else {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      return null;
    }
  }

  if (response.status === 401) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`${response.status}: ${response.statusText}`);
  }

  return response.json();
}

async function logout(): Promise<void> {
  try {
    // Call backend to clear server-side session/cookies
    await fetch(apiUrl("/logout"));
  } catch (error) {
    console.error("Logout error:", error);
  } finally {
    // Always clear local tokens
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

export function useAuth() {
  const queryClient = useQueryClient();
  const { data: user, isLoading } = useQuery<User | null>({
    queryKey: ["/api/auth/user"],
    queryFn: fetchUser,
    retry: false,
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnReconnect: true,
  });

  const logoutMutation = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      queryClient.setQueryData(["/api/auth/user"], null);
      queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
    },
  });

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    logout: logoutMutation.mutate,
    isLoggingOut: logoutMutation.isPending,
  };
}

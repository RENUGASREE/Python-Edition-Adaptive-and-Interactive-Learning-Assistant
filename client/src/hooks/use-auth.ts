import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { User } from "@/types";
import { apiUrl, getAccessToken, getRefreshToken, storeTokens, clearTokens } from "@/lib/api";

async function fetchUser(): Promise<User | null> {
  const accessToken = getAccessToken();
  const refreshToken = getRefreshToken();
  
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
        storeTokens(data.access, data.refresh ?? refreshToken);
        response = await attemptFetch(data.access);
      }
    } else {
      clearTokens();
      return null;
    }
  }

  if (response.status === 401) {
    clearTokens();
    return null;
  }

  if (!response.ok) {
    // For other errors, return null instead of throwing to avoid console noise for unauthenticated users
    return null;
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
    clearTokens();
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

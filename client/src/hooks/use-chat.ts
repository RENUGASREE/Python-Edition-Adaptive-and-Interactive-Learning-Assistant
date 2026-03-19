import { useState, useCallback } from "react";
import { apiUrl } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
  sourceTopic?: string | null;
  confidenceScore?: number | null;
}

interface TutorContext {
  lessonTitle?: string;
  lessonContent?: string;
}

export function useChat(context?: TutorContext) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    setIsLoading(true);
    setMessages((prev) => [...prev, { role: "user", content }]);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 45000); // Increased to 45s for AI responses
      // Prepare short history (last 4 messages + current) to give the backend context
      const historyToSend = [...messages.slice(-4), { role: "user", content }].map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const response = await fetch(apiUrl("/ai-tutor"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: content, topic: context?.lessonTitle, history: historyToSend }),
        credentials: "include",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Server error: ${response.status}`);
      }
      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data?.response || "AI is currently unavailable",
          sourceTopic: data?.source || null,
          confidenceScore: null,
        },
      ]);
    } catch (error: any) {
      console.error("Chat error:", error);
      let errText = "AI is currently unavailable";
      if (error?.name === "AbortError") errText = "AI response timed out. Try again later.";
      setMessages((prev) => [...prev, { role: "assistant", content: errText }]);
    } finally {
      setIsLoading(false);
    }
  }, [context, messages]);

  return { messages, sendMessage, isLoading, setMessages };
}

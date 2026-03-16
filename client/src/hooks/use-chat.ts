import { useState, useCallback } from "react";
import { apiUrl, getAccessToken } from "@/lib/api";

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

function buildTutorResponse(message: string, context?: TutorContext) {
  const title = context?.lessonTitle ? `**${context.lessonTitle}**` : "this topic";
  const content = context?.lessonContent || "";
  const codeMatch = content.match(/```(?:python)?\n([\s\S]*?)```/);
  const codeSnippet = codeMatch?.[1]?.trim();
  const plain = content.replace(/```[\s\S]*?```/g, "").replace(/#/g, "");
  const lines = plain.split("\n").map((line) => line.trim()).filter(Boolean);
  const keyIdea = lines[0] || "Focus on the goal and the expected output.";
  const shortSummary = lines.slice(1, 4).join(" ");
  const lower = message.toLowerCase();
  let response = `Here is a focused hint for ${title}.\n\nKey idea: ${keyIdea}`;
  if (shortSummary) response += `\n\n${shortSummary}`;
  if ((lower.includes("example") || lower.includes("syntax") || lower.includes("how") || lower.includes("code")) && codeSnippet) {
    response += `\n\n\`\`\`python\n${codeSnippet}\n\`\`\``;
  }
  if (lower.includes("quiz") || lower.includes("placement") || lower.includes("personal")) {
    response += "\n\nYour placement quiz result shapes your starting point and practice suggestions. As you complete lessons, the system adapts what you see next.";
  }
  response += "\n\nShare the exact error or the output you expected if you want a more precise fix.";
  return response;
}

export function useChat(context?: TutorContext) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    setIsLoading(true);
    setMessages((prev) => [...prev, { role: "user", content }]);

    try {
      const accessToken = getAccessToken();
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 45000); // Increased to 45s for AI responses

      const response = await fetch(apiUrl("/ai-tutor"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ query: content, topic: context?.lessonTitle }),
        credentials: "include",
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Server error: ${response.status}`);
      }
      const data = await response.json();
      const fallback = buildTutorResponse(content, context);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data?.response || fallback,
          sourceTopic: data?.source_topic || null,
          confidenceScore: data?.confidence_score ?? null,
        },
      ]);
    } catch (error: any) {
      console.error("Chat error:", error);
      let content = "AI tutor is temporarily unavailable.";
      if (error?.message) {
        if (error.message.includes("401")) content = "Session expired. Please log in again.";
        else if (error.name === "AbortError") content = "AI response timed out. Try again with a shorter question.";
        else content = `AI Tutor error: ${error.message}`;
      }
      setMessages((prev) => [...prev, { role: "assistant", content }]);
    } finally {
      setIsLoading(false);
    }
  }, [context]);

  return { messages, sendMessage, isLoading, setMessages };
}

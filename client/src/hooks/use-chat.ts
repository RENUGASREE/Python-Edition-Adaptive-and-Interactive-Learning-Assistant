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
      const accessToken = localStorage.getItem("access_token");
      const response = await fetch(apiUrl("/ai-tutor"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ query: content, topic: context?.lessonTitle }),
        credentials: "include",
      });

      if (!response.ok) throw new Error("Failed to send message");
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
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [...prev, { role: "assistant", content: "AI tutor is temporarily unavailable." }]);
    } finally {
      setIsLoading(false);
    }
  }, [context]);

  return { messages, sendMessage, isLoading, setMessages };
}

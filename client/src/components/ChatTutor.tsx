import { useState, useRef, useEffect } from "react";
import { useChat } from "@/hooks/use-chat";
import { Send, Bot, User, Loader2, Sparkles, X } from "lucide-react";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";

interface ChatTutorProps {
  lessonId: number;
  lessonTitle: string;
  lessonContent: string;
}

export function ChatTutor({ lessonId, lessonTitle, lessonContent }: ChatTutorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const conversationKey = lessonId;

  return (
    <>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(true)}
        className={cn(
          "fixed bottom-6 right-6 p-4 rounded-full shadow-xl z-50 transition-all duration-300 hover:scale-105",
          "bg-gradient-to-r from-primary to-accent text-primary-foreground",
          isOpen && "opacity-0 pointer-events-none scale-0"
        )}
      >
        <Sparkles className="w-6 h-6" />
      </button>

      {/* Chat Window */}
      <div className={cn(
        "fixed bottom-6 right-6 w-96 max-w-[calc(100vw-3rem)] h-[500px] bg-card border border-border rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden transition-all duration-300 origin-bottom-right",
        isOpen ? "scale-100 opacity-100" : "scale-0 opacity-0 pointer-events-none"
      )}>
        {/* Header */}
        <div className="p-4 bg-muted/50 border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-primary/20 p-1.5 rounded-lg">
              <Bot className="w-4 h-4 text-primary" />
            </div>
            <div>
              <h3 className="font-bold text-sm">AI Tutor</h3>
              <p className="text-xs text-muted-foreground">Ask for help or hints</p>
            </div>
          </div>
          <button 
            onClick={() => setIsOpen(false)}
            className="p-1 hover:bg-background rounded-full transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Conversation */}
        <ChatConversation
          conversationKey={conversationKey}
          lessonTitle={lessonTitle}
          lessonContent={lessonContent}
        />
      </div>
    </>
  );
}

function ChatConversation({
  conversationKey,
  lessonTitle,
  lessonContent,
}: {
  conversationKey: number;
  lessonTitle: string;
  lessonContent: string;
}) {
  const { messages, sendMessage, isLoading, setMessages } = useChat({ lessonTitle, lessonContent });
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, conversationKey]);

  useEffect(() => {
    setMessages([]);
  }, [conversationKey, setMessages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <>
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground text-sm py-8 px-4">
            <p>👋 Hi there! I'm your Python tutor.</p>
            <p className="mt-2">Stuck on a problem? Need a hint? Just ask!</p>
          </div>
        )}
        
        {messages.map((msg, i) => (
          <div
            key={i}
            className={cn(
              "flex gap-3 max-w-[85%]",
              msg.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            )}
          >
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
              msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
            )}>
              {msg.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>
            <div className={cn(
              "p-3 rounded-2xl text-sm leading-relaxed",
              msg.role === "user" 
                ? "bg-primary text-primary-foreground rounded-tr-sm" 
                : "bg-muted rounded-tl-sm markdown-content"
            )}>
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              {msg.role === "assistant" && (msg.sourceTopic || msg.confidenceScore !== null) && (
                <div className="mt-3 text-xs text-muted-foreground flex items-center gap-3">
                  {msg.sourceTopic && <span>Source: {msg.sourceTopic}</span>}
                  {msg.confidenceScore !== null && msg.confidenceScore !== undefined && (
                    <span>Confidence: {Math.round((msg.confidenceScore || 0) * 100)}%</span>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3 mr-auto max-w-[85%]">
            <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-muted-foreground" />
            </div>
            <div className="bg-muted p-3 rounded-2xl rounded-tl-sm flex items-center">
              <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-3 border-t border-border bg-background">
        <div className="relative">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..."
            className="w-full pl-4 pr-12 py-3 bg-muted/50 border border-transparent focus:border-primary rounded-xl text-sm focus:outline-none focus:ring-1 focus:ring-primary/20 transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 top-2 p-1.5 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </>
  );
}

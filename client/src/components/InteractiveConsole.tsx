import React, { useState, useRef, useEffect } from 'react';
import { AlertCircle, Send } from 'lucide-react';

interface ConsoleEvent {
  type: 'output' | 'prompt' | 'input' | 'error';
  content: string;
}

interface InteractiveConsoleProps {
  events: ConsoleEvent[];
  isRunning: boolean;
  onInput: (input: string) => void;
  error?: string;
}

export function InteractiveConsole({ events, isRunning, onInput, error }: InteractiveConsoleProps) {
  const [inputValue, setInputValue] = useState('');
  const [waitingForInput, setWaitingForInput] = useState(false);
  const consoleRef = useRef<HTMLDivElement>(null);

  // Check if last event is a prompt waiting for input
  useEffect(() => {
    const lastEvent = events[events.length - 1];
    if (lastEvent && lastEvent.type === 'prompt') {
      setWaitingForInput(true);
      setInputValue('');
    }
  }, [events]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [events]);

  const handleSubmitInput = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() || isRunning) {
      onInput(inputValue);
      setWaitingForInput(false);
      setInputValue('');
    }
  };

  const isEmpty = !error && events.length === 0;

  return (
    <div className="h-full bg-[#0f0f0f] flex flex-col">
      {/* Console Header */}
      <div className="h-8 bg-[#1e1e1e] border-b border-[#333] px-4 flex items-center text-xs font-mono text-muted-foreground uppercase tracking-wider">
        Console Output
      </div>

      {/* Console Display Area */}
      <div 
        ref={consoleRef}
        className="flex-1 p-4 font-mono text-sm overflow-auto bg-[#0f0f0f]"
      >
        {error ? (
          <div className="text-red-400 whitespace-pre-wrap flex gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            {error}
          </div>
        ) : isEmpty ? (
          <div className="text-gray-600 italic">Run your code to see output...</div>
        ) : (
          <div className="space-y-0">
            {events.map((event, idx) => (
              <div key={idx} className="text-gray-100">
                {event.type === 'prompt' && (
                  <span className="text-yellow-400">{event.content}</span>
                )}
                {event.type === 'input' && (
                  <span className="text-cyan-400">{event.content}</span>
                )}
                {event.type === 'output' && (
                  <span className="text-green-400">{event.content}</span>
                )}
                {event.type === 'error' && (
                  <span className="text-red-400">{event.content}</span>
                )}
                {'\n'}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Input Area */}
      {waitingForInput && (
        <form onSubmit={handleSubmitInput} className="border-t border-[#333] bg-[#1e1e1e] p-3">
          <div className="flex gap-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Enter input..."
              autoFocus
              className="flex-1 bg-[#2d2d30] text-gray-100 px-3 py-1 rounded border border-[#333] text-xs focus:outline-none focus:border-blue-500"
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs flex items-center gap-1 transition-colors"
            >
              <Send className="w-3 h-3" />
              Send
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

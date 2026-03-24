import React, { useRef, useEffect, useState } from 'react';
import { AlertCircle, Send } from 'lucide-react';
import { formatConsoleOutput } from '@/lib/console-formatter';

interface TerminalConsoleProps {
  output: string;
  error?: string;
  isRunning?: boolean;
}

interface InteractiveConsoleProps {
  isWaitingForInput: boolean;
  onInputSubmit: (value: string) => void;
  output: string;
  error?: string;
  isRunning?: boolean;
  prompts?: string[];
  currentPromptIndex?: number;
}

export function TerminalConsole({ output, error, isRunning }: TerminalConsoleProps) {
  const consoleRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [output, error]);

  const isEmpty = !error && !output;
  const formatted = output ? formatConsoleOutput(output) : { lines: [] };

  return (
    <div className="h-full bg-[#0f0f0f] flex flex-col">
      {/* Console Header */}
      <div className="h-8 bg-[#1e1e1e] border-b border-[#333] px-4 flex items-center text-xs font-mono text-muted-foreground uppercase tracking-wider justify-between">
        <span>Console Output</span>
        {isRunning && <span className="animate-pulse text-yellow-500 text-[10px]">Running...</span>}
      </div>

      {/* Console Display Area */}
      <div 
        ref={consoleRef}
        className="flex-1 p-4 font-mono text-sm overflow-auto bg-[#0f0f0f] overflow-x-hidden"
      >
        {error ? (
          <div className="text-red-400 whitespace-pre-wrap">
            <div className="flex gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 flex-shrink-0" />
              <div>{error}</div>
            </div>
          </div>
        ) : isEmpty ? (
          <div className="text-gray-600 italic">Run your code to see output...</div>
        ) : (
          <div className="space-y-0">
            {formatted.lines.map((line, idx) => (
              <div key={idx} className={line.className}>
                {line.text || '\u00A0'}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Interactive console that shows prompts one at a time
 * Waits for user input before showing next prompt
 */
export function InteractiveConsole({
  isWaitingForInput,
  onInputSubmit,
  output,
  error,
  isRunning,
  prompts,
  currentPromptIndex,
}: InteractiveConsoleProps) {
  const [inputValue, setInputValue] = useState('');
  const consoleRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const currentPrompt = prompts?.[currentPromptIndex ?? 0] || '';
  const promptLabel = currentPrompt || `Input #${(currentPromptIndex ?? 0) + 1}`;

  // Auto-scroll and focus when waiting for input
  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [output, error]);

  useEffect(() => {
    if (isWaitingForInput && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isWaitingForInput]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue !== undefined) {
      onInputSubmit(inputValue);
      setInputValue('');
    }
  };

  const isEmpty = !error && !output;

  return (
    <div className="h-full bg-[#0f0f0f] flex flex-col">
      {/* Console Header */}
      <div className="h-8 bg-[#1e1e1e] border-b border-[#333] px-4 flex items-center text-xs font-mono text-muted-foreground uppercase tracking-wider justify-between">
        <span>Interactive Console</span>
        {isRunning && <span className="animate-pulse text-yellow-500 text-[10px]">Running...</span>}
      </div>

      {/* Console Display Area */}
      <div 
        ref={consoleRef}
        className="flex-1 p-4 font-mono text-sm overflow-auto bg-[#0f0f0f] overflow-x-hidden space-y-1"
      >
        {error ? (
          <div className="text-red-400 whitespace-pre-wrap">
            <div className="flex gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 flex-shrink-0" />
              <div>{error}</div>
            </div>
          </div>
        ) : isEmpty ? (
          <div className="text-gray-600 italic">Run your code to start interactive execution...</div>
        ) : (
          <div className="space-y-0">
            {output.split('\n').map((line, idx) => {
              const trimmed = line.trim();
              const isPromptLine =
                !!(line && (trimmed.endsWith(':') || trimmed.endsWith('?'))); // treats prompt-style lines as prompt

              return (
                <div key={idx}>
                  {isPromptLine ? (
                    <span className="text-yellow-300 font-semibold">{line}</span>
                  ) : line.toLowerCase().includes('error') || line.toLowerCase().includes('traceback') ? (
                    <span className="text-red-400">{line}</span>
                  ) : (
                    <span className="text-green-400">{line}</span>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Input Area - Shows when waiting for input */}
      {isWaitingForInput && (
        <form onSubmit={handleSubmit} className="border-t border-[#333] bg-[#1e1e1e] p-3 space-y-2">
          <div className="flex gap-2 items-center">
            <span className="text-yellow-300 font-semibold text-xs">»</span>
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={
                currentPrompt
                  ? `${currentPrompt.trim()} (type your answer and press Enter)`
                  : 'Type input and press Enter...'
              }
              className="flex-1 bg-[#0f0f0f] text-green-400 px-2 py-1 rounded border border-[#333] text-xs focus:outline-none focus:border-yellow-500 font-mono"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleSubmit(e as any);
                }
              }}
            />
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white p-1 rounded text-xs transition-colors"
            >
              <Send className="w-3 h-3" />
            </button>
          </div>
        </form>
      )}
    </div>
  );
}

/**
 * Alternative: Interactive multi-step console
 * Shows one input at a time for a true interactive experience
 */
export function StepwiseInteractiveConsole({
  code,
  onRunWithInputs,
}: {
  code: string;
  onRunWithInputs: (inputs: string[]) => Promise<{ output: string; error?: string }>;
}) {
  const [step, setStep] = React.useState<'idle' | 'running' | 'awaiting_input'>('idle');
  const [inputs, setInputs] = React.useState<string[]>([]);
  const [currentInputIndex, setCurrentInputIndex] = React.useState(0);
  const [output, setOutput] = React.useState('');
  const [error, setError] = React.useState<string>();
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Detect input() calls in code
  const inputCount = (code.match(/input\s*\(/g) || []).length;

  const handleSubmitInput = async (value: string) => {
    const newInputs = [...inputs, value];
    setInputs(newInputs);

    if (newInputs.length < inputCount) {
      // Move to next input
      setCurrentInputIndex(newInputs.length);
      setStep('awaiting_input');
      setTimeout(() => inputRef.current?.focus(), 100);
    } else {
      // All inputs collected, run code
      setStep('running');
      try {
        const result = await onRunWithInputs(newInputs);
        setOutput(result.output);
        setError(result.error);
        setStep('idle');
      } catch (err: any) {
        setError(err.message);
        setStep('idle');
      }
    }
  };

  const reset = () => {
    setStep('idle');
    setInputs([]);
    setCurrentInputIndex(0);
    setOutput('');
    setError(undefined);
  };

  return (
    <div className="h-full bg-[#0f0f0f] flex flex-col">
      <div className="h-8 bg-[#1e1e1e] border-b border-[#333] px-4 flex items-center text-xs font-mono text-muted-foreground uppercase tracking-wider">
        Interactive Console
      </div>

      <div className="flex-1 p-4 font-mono text-sm overflow-auto space-y-2">
        {output && (
          <div className="text-green-400 whitespace-pre-wrap">{output}</div>
        )}
        {error && (
          <div className="text-red-400 whitespace-pre-wrap">{error}</div>
        )}
        {!output && !error && (
          <div className="text-gray-600 italic">
            {inputCount > 0
              ? `Code needs ${inputCount} input(s). Click "Run" to start.`
              : 'Click "Run" to execute code.'}
          </div>
        )}
      </div>

      {/* Input Collection */}
      {step === 'idle' && inputCount > 0 && (
        <div className="border-t border-[#333] bg-[#1e1e1e] p-3 space-y-2">
          <button
            onClick={() => {
              setStep('awaiting_input');
              setCurrentInputIndex(0);
              setTimeout(() => inputRef.current?.focus(), 100);
            }}
            className="w-full bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded text-xs font-mono transition-colors"
          >
            Run Code (Waiting for {inputCount} Input{inputCount > 1 ? 's' : ''})
          </button>
        </div>
      )}

      {step === 'awaiting_input' && currentInputIndex < inputCount && (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const value = inputRef.current?.value || '';
            handleSubmitInput(value);
            if (inputRef.current) inputRef.current.value = '';
          }}
          className="border-t border-[#333] bg-[#1e1e1e] p-3 space-y-2"
        >
          <label className="text-xs text-gray-400">
            Input {currentInputIndex + 1} of {inputCount}
          </label>
          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              placeholder={`Enter input ${currentInputIndex + 1}...`}
              autoFocus
              className="flex-1 bg-[#2d2d30] text-gray-100 px-3 py-1 rounded border border-[#333] text-xs focus:outline-none focus:border-blue-500"
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs transition-colors"
            >
              Submit
            </button>
          </div>
        </form>
      )}

      {(step === 'running' || (output && currentInputIndex === inputCount)) && (
        <div className="border-t border-[#333] bg-[#1e1e1e] p-3">
          <button
            onClick={reset}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded text-xs font-mono transition-colors"
          >
            Run Again
          </button>
        </div>
      )}
    </div>
  );
}

import { Layout } from "@/components/Layout";
import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useState } from "react";
import { useRunChallenge } from "@/hooks/use-lessons";
import { Loader2 } from "lucide-react";
import { formatConsoleOutput, getConsoleHelpText } from "@/lib/console-formatter";
import { InteractiveConsole } from "@/components/TerminalConsole";
import { parseInputCalls, getInputCount, formatInteractiveOutput, stripInputPromptsFromOutput } from "@/lib/interactive-console";

type Challenge = {
  id: number;
  title: string;
  description: string;
  difficulty?: string | null;
  initialCode: string;
  solutionCode?: string | null;
  testCases: any;
};

export default function Challenges() {
  const { data, isLoading } = useQuery({
    queryKey: ["/api/challenges"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/challenges/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch challenges");
      return res.json() as Promise<Challenge[]>;
    },
  });
  const [selected, setSelected] = useState<Challenge | null>(null);
  const run = useRunChallenge();
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showSolution, setShowSolution] = useState(false);

  // Interactive mode state
  const [isInteractiveMode, setIsInteractiveMode] = useState(false);
  const [isWaitingForInput, setIsWaitingForInput] = useState(false);
  const [collectedInputs, setCollectedInputs] = useState<string[]>([]);
  const [interactiveOutput, setInteractiveOutput] = useState("");
  const [totalInputsNeeded, setTotalInputsNeeded] = useState(0);
  const [inputCalls, setInputCalls] = useState<any[]>([]);
  const [currentInputIndex, setCurrentInputIndex] = useState(0);

  const groups: Record<string, Challenge[]> = { Easy: [], Medium: [], Hard: [] };
  (data || []).forEach((c) => {
    // Only include standalone challenges (lesson_id is -1 or not associated with a lesson)
    // This ensures we have exactly 10 per category
    const d = (c.difficulty || "").toLowerCase();
    if (d.includes("beginner") || d.includes("easy")) groups.Easy.push(c);
    else if (d.includes("intermediate") || d.includes("medium")) groups.Medium.push(c);
    else if (d.includes("advanced") || d.includes("hard") || d.includes("pro")) groups.Hard.push(c);
    // Default to Easy if no difficulty specified
    else groups.Easy.push(c);
  });
  
  // Limit to 10 per category
  Object.keys(groups).forEach(key => {
    groups[key] = groups[key].slice(0, 10);
  });

  const handleSelect = (c: Challenge) => {
    setSelected(c);
    setCode(c.initial_code || "");
    setOutput("");
    setError(null);
    setShowSolution(false);
  };

  const handleRun = async () => {
    if (!selected) return;
    
    // Check for input() calls
    const inputCount = getInputCount(code);
    
    if (inputCount > 0) {
      // Interactive mode
      const calls = parseInputCalls(code);
      setInputCalls(calls);
      setTotalInputsNeeded(inputCount);
      setCollectedInputs([]);
      setCurrentInputIndex(0);
      setInteractiveOutput("");
      setError(null);
      setOutput("");
      setIsInteractiveMode(true);
      setIsWaitingForInput(true);
    } else {
      // Non-interactive mode
      setIsInteractiveMode(false);
      try {
        setOutput("Running...");
        setError(null);
        const result = await run.mutateAsync({ id: selected.id, code, input: "" });
        // Show the actual output from code execution
        if (result.output) {
          setOutput(result.output);
        } else {
          setOutput("");
        }
        if (result.error) {
          setError(result.error);
        } else if (result.passed) {
          setOutput((prev) => (prev ? prev + "\n\n" : "") + "✅ Challenge completed successfully!");
        }
      } catch (e: any) {
        setError(e?.message || "Failed to run");
        setOutput("");
      }
    }
  };

  const handleInteractiveInput = async (value: string) => {
    if (!selected) return;
    
    const newInputs = [...collectedInputs, value];
    setCollectedInputs(newInputs);
    
    // Add to display output
    const inputCall = inputCalls[currentInputIndex];
    const prompt = inputCall?.prompt || "Input";
    const displayOutput = interactiveOutput + prompt + "\n" + value + "\n";
    setInteractiveOutput(displayOutput);
    
    if (newInputs.length < totalInputsNeeded) {
      // More inputs needed
      setCurrentInputIndex(newInputs.length);
      setIsWaitingForInput(true);
    } else {
      // All inputs collected, run code
      setIsWaitingForInput(false);
      setOutput("Running...");
      
      try {
        const result = await run.mutateAsync({
          id: selected.id,
          code,
          input: newInputs.join('\n')
        });

        const cleanedRuntimeOutput = stripInputPromptsFromOutput(
          result.output || "",
          inputCalls.map((c) => c.prompt || "")
        );

        const finalOutput = formatInteractiveOutput(
          inputCalls.map((c) => c.prompt || ""),
          newInputs,
          cleanedRuntimeOutput
        );

        setInteractiveOutput(finalOutput);
        setOutput(finalOutput);

        if (result.error) {
          setError(result.error);
        } else if (result.passed) {
          setError(null);
          setOutput((prev) => (prev ? prev + "\n\n" : "") + "✅ Challenge completed successfully!");
        }
      } catch (e: any) {
        setError(e?.message || "Failed to run");
      } finally {
        setIsInteractiveMode(false);
      }
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full py-16">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto py-8 px-4 grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <h1 className="text-2xl font-bold">Interview Challenges</h1>
          {["Easy", "Medium", "Hard"].map((key) => (
            <div key={key}>
              <div className="text-sm font-semibold mb-2">{key}</div>
              <div className="space-y-2">
                {groups[key].length === 0 && <div className="text-sm text-muted-foreground">No challenges</div>}
                {groups[key].map((c) => (
                  <button
                    key={c.id}
                    onClick={() => handleSelect(c)}
                    className="w-full text-left p-3 rounded-lg border border-border hover:border-primary/50"
                  >
                    <div className="font-medium">{c.title}</div>
                    <div className="text-xs text-muted-foreground">{c.description}</div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-bold">Challenge Runner</h2>
          {!selected ? (
            <div className="text-sm text-muted-foreground">Select a challenge to start.</div>
          ) : (
            <div className="space-y-4">
              <div className="p-4 rounded-lg border border-border">
                <div className="font-semibold">{selected.title}</div>
                <div className="text-sm text-muted-foreground mt-1">{selected.description}</div>
              </div>
              <textarea
                className="w-full h-64 p-3 rounded-lg border border-border bg-muted"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
                placeholder="Write your Python code here..."
              />
              <div className="flex gap-3">
                <button
                  onClick={handleRun}
                  disabled={run.isPending}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-lg disabled:opacity-50"
                >
                  {run.isPending ? "Running..." : "Run Code"}
                </button>
                {selected.solutionCode && (
                  <button
                    onClick={() => setShowSolution(!showSolution)}
                    className="px-4 py-2 border border-border rounded-lg text-sm hover:bg-muted"
                  >
                    {showSolution ? "Hide Answer" : "Show Answer"}
                  </button>
                )}
              </div>
              {showSolution && selected.solutionCode && (
                <div className="p-4 rounded-lg bg-accent/10 border border-accent/20">
                  <div className="text-sm font-semibold mb-2">Reference Solution</div>
                  <pre className="text-xs font-mono text-accent whitespace-pre-wrap">{selected.solutionCode}</pre>
                </div>
              )}
              
              {isInteractiveMode ? (
                <InteractiveConsole 
                  isWaitingForInput={isWaitingForInput}
                  onInputSubmit={handleInteractiveInput}
                  output={interactiveOutput}
                  error={error || undefined}
                  isRunning={run.isPending}
                  prompts={inputCalls.map((c) => c.prompt || "")}
                  currentPromptIndex={currentInputIndex}
                />
              ) : (
                <div className="p-3 rounded-lg border border-border bg-[#0f0f0f]">
                  <div className="text-sm font-medium mb-2">Output</div>
                  <div className="text-xs text-gray-400 mb-2">{getConsoleHelpText(code)}</div>
                  <div className="font-mono text-xs whitespace-pre-wrap">
                    {output ? (
                      formatConsoleOutput(output).lines.map((line, idx) => (
                        <div key={idx} className={line.className}>
                          {line.text || '\u00A0'}
                        </div>
                      ))
                    ) : (
                      <span className="text-gray-600">Click "Run Code" to see output...</span>
                    )}
                  </div>
                  {error && <div className="text-xs text-red-400 mt-2">Error: {error}</div>}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

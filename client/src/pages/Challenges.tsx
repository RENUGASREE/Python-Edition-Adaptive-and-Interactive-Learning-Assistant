import { Layout } from "@/components/Layout";
import { useQuery } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { useState } from "react";
import { useRunChallenge } from "@/hooks/use-lessons";
import { Loader2 } from "lucide-react";

type Challenge = {
  id: number;
  title: string;
  description: string;
  difficulty?: string | null;
  initialCode: string;
  testCases: any;
};

export default function Challenges() {
  const { data, isLoading } = useQuery({
    queryKey: ["/api/challenges"],
    queryFn: async () => {
      const accessToken = localStorage.getItem("access_token");
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

  const groups: Record<string, Challenge[]> = { Easy: [], Medium: [], Hard: [], Other: [] };
  (data || []).forEach((c) => {
    const d = (c.difficulty || "").toLowerCase();
    if (d.includes("easy")) groups.Easy.push(c);
    else if (d.includes("medium")) groups.Medium.push(c);
    else if (d.includes("hard")) groups.Hard.push(c);
    else groups.Other.push(c);
  });

  const handleSelect = (c: Challenge) => {
    setSelected(c);
    setCode(c.initialCode || "");
    setOutput("");
    setError(null);
  };

  const handleRun = async () => {
    if (!selected) return;
    try {
      setOutput("Running...");
      setError(null);
      const result = await run.mutateAsync({ id: selected.id, code });
      setOutput(result.output || "");
      if (result.error) setError(result.error);
    } catch (e: any) {
      setError(e?.message || "Failed to run");
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
          {["Easy", "Medium", "Hard", "Other"].map((key) => (
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
              />
              <div className="flex gap-3">
                <button
                  onClick={handleRun}
                  disabled={run.isPending}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-lg disabled:opacity-50"
                >
                  {run.isPending ? "Running..." : "Run Code"}
                </button>
              </div>
              <div className="p-3 rounded-lg border border-border">
                <div className="text-sm font-medium">Output</div>
                <pre className="text-xs whitespace-pre-wrap mt-2">{output || " "}</pre>
                {error && <div className="text-xs text-destructive mt-2">{error}</div>}
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

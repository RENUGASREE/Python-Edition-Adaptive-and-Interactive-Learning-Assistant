import { Layout } from "@/components/Layout";
import { useAnalytics } from "@/hooks/use-analytics";
import { Loader2 } from "lucide-react";
import { useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Cell, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";
import { useAuth } from "@/hooks/use-auth";


export default function Analytics() {
  const { analytics, isLoading } = useAnalytics();
  const { user } = useAuth();

  const chartData = useMemo(() => {
    if (!analytics?.masteryProgression) return [];
    return analytics.masteryProgression.map((entry) => ({
      date: new Date(entry.created_at).toLocaleDateString(),
      score: Math.round(entry.overall_score * 100),
    }));
  }, [analytics]);

  const gainData = useMemo(() => {
    if (!analytics?.masteryProgression || analytics.masteryProgression.length < 2) {
      return [];
    }
    const first = analytics.masteryProgression[0];
    const last = analytics.masteryProgression[analytics.masteryProgression.length - 1];
    return [
      { label: "Pre-test", score: Math.round((first.overall_score || 0) * 100) },
      { label: "Post-test", score: Math.round((last.overall_score || 0) * 100) },
    ];
  }, [analytics]);

  const engagementPercent = Math.round((analytics?.engagementIndex || 0) * 100);
  const riskPercent = Math.round((analytics?.riskScore || 0) * 100);
  const masteryRadar = useMemo(() => {
    const mv = (user as any)?.masteryVector || (user as any)?.mastery_vector || {};
    return Object.entries(mv).slice(0, 8).map(([topic, score]) => ({
      topic: String(topic),
      value: Math.round(Number(score) * 100),
    }));
  }, [user]);

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-8 py-10 px-4">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">Learning Analytics</h1>
          <p className="text-muted-foreground">Track mastery progression, engagement, and risk signals.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground">Learning Gain</div>
            <div className="text-3xl font-bold">{Math.round((analytics?.learningGain || 0) * 100)}%</div>
          </div>
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground">Engagement Index</div>
            <div className="text-3xl font-bold">{engagementPercent}%</div>
          </div>
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground">Risk Score</div>
            <div className="text-3xl font-bold">{riskPercent}%</div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground mb-4">Mastery Progression</div>
            <div className="h-[280px]">
              {chartData.length < 2 ? (
                <div className="text-sm text-muted-foreground flex items-center justify-center h-full">
                  Not enough data yet
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
                    <YAxis domain={[0, 100]} stroke="#64748b" fontSize={12} />
                    <Tooltip />
                    <Line type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
          <div className="bg-card border border-border rounded-2xl p-6">
            <div className="text-sm text-muted-foreground mb-4">Pre-test vs Post-test</div>
            <div className="h-[280px]">
              {gainData.length < 2 ? (
                <div className="text-sm text-muted-foreground flex items-center justify-center h-full">
                  Not enough data yet
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={gainData}>
                    <XAxis dataKey="label" stroke="#64748b" fontSize={12} />
                    <YAxis domain={[0, 100]} stroke="#64748b" fontSize={12} />
                    <Tooltip />
                    <Bar dataKey="score" radius={[8, 8, 0, 0]}>
                      {gainData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={index === 1 ? "hsl(var(--primary))" : "hsl(var(--muted))"} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-2xl p-6">
          <div className="text-sm text-muted-foreground mb-4">Skill Mastery per Topic</div>
          <div className="h-[320px]">
            {masteryRadar.length === 0 ? (
              <div className="text-sm text-muted-foreground flex items-center justify-center h-full">
                Not enough data yet
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={masteryRadar}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="topic" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar name="Mastery" dataKey="value" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.3} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
            <div className="text-sm text-muted-foreground">Weakest vs Strongest</div>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-xs text-muted-foreground">Weakest</div>
                <div className="text-lg font-semibold">{analytics?.weakestTopic || "Not enough data"}</div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Strongest</div>
                <div className="text-lg font-semibold">{analytics?.strongestTopic || "Not enough data"}</div>
              </div>
            </div>
            <div className="text-sm text-muted-foreground">Focus practice on the weakest topic to raise mastery.</div>
          </div>
          <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
            <div className="text-sm text-muted-foreground">Engagement Meter</div>
            <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
              <div className="h-full bg-primary" style={{ width: `${engagementPercent}%` }} />
            </div>
            <div className="text-sm text-muted-foreground">
              {riskPercent > 60 ? "Risk alert: low mastery and engagement detected." : "Engagement is stable."}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

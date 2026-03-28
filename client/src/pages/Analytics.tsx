import { Layout } from "@/components/Layout";
import { useAnalytics } from "@/hooks/use-analytics";
import { Loader2, TrendingUp, Zap, AlertTriangle, BookOpen, Star, Target, Hexagon } from "lucide-react";
import { useMemo, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  CartesianGrid,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";
import { useAuth } from "@/hooks/use-auth";

// ── Custom Tooltip ─────────────────────────────────────────────────────────────
const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-card border border-border rounded-xl px-4 py-3 shadow-lg text-sm">
      <p className="text-muted-foreground mb-1">{label}</p>
      <p className="font-bold text-primary text-lg">{payload[0].value}%</p>
      <p className="text-xs text-muted-foreground">Mastery Score</p>
    </div>
  );
};

// ── Stat Card ──────────────────────────────────────────────────────────────────
function StatCard({
  icon: Icon,
  label,
  value,
  subtitle,
  color,
}: {
  icon: React.ElementType;
  label: string;
  value: string;
  subtitle: string;
  color: string;
}) {
  return (
    <div className="bg-card border border-border rounded-2xl p-6 flex flex-col gap-3 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-muted-foreground">{label}</span>
        <div className={`p-2 rounded-xl ${color}`}>
          <Icon className="w-4 h-4 text-white" />
        </div>
      </div>
      <div className="text-4xl font-extrabold tracking-tight">{value}</div>
      <p className="text-xs text-muted-foreground leading-relaxed">{subtitle}</p>
    </div>
  );
}

// ── Main Component ─────────────────────────────────────────────────────────────
export default function Analytics() {
  const { analytics, isLoading } = useAnalytics();
  const { user } = useAuth();

  // Progress-over-time series
  const chartData = useMemo(() => {
    if (!analytics?.masteryProgression || analytics.masteryProgression.length === 0) return [];
    return analytics.masteryProgression.map((entry: any, idx: number) => ({
      date: new Date(entry.created_at).toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
      }),
      score: Math.round((entry.overall_score || 0) * 100),
      index: idx,
    }));
  }, [analytics]);

  const milestones = useMemo(() => {
    const marks: { index: number; label: string; color: string }[] = [];
    let crossed50 = false;
    let crossed80 = false;
    chartData.forEach((d, i) => {
      if (!crossed50 && d.score >= 50) {
        marks.push({ index: i, label: "50% Milestone", color: "#f59e0b" });
        crossed50 = true;
      }
      if (!crossed80 && d.score >= 80) {
        marks.push({ index: i, label: "80% Milestone", color: "#22c55e" });
        crossed80 = true;
      }
    });
    return marks;
  }, [chartData]);

  const skillTopics = useMemo(() => {
    const mv = (user as any)?.masteryVector || (user as any)?.mastery_vector || {};
    return Object.entries(mv)
      .map(([topic, score]) => ({
        topic: String(topic).replace(/_/g, " "),
        value: Math.round(Number(score) * 100),
        fullMark: 100,
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 8);
  }, [user]);

  const engagementPercent = Math.round((analytics?.engagementIndex || 0) * 100);
  const riskPercent = Math.round((analytics?.riskScore || 0) * 100);
  const learningGain = Math.round((analytics?.learningGain || 0) * 100);

  const trend = useMemo(() => {
    if (chartData.length < 4) return null;
    const mid = Math.floor(chartData.length / 2);
    const firstHalfAvg = chartData.slice(0, mid).reduce((s, d) => s + d.score, 0) / mid;
    const secondHalfAvg = chartData.slice(mid).reduce((s, d) => s + d.score, 0) / (chartData.length - mid);
    const delta = Math.round(secondHalfAvg - firstHalfAvg);
    return delta;
  }, [chartData]);

  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full min-h-[60vh]">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto space-y-8 py-10 px-4">
        {/* Header */}
        <div className="space-y-1">
          <h1 className="text-3xl font-extrabold tracking-tight">Learning Analytics</h1>
          <p className="text-muted-foreground text-sm">
            Your personalised mastery journey — visualised over time.
          </p>
        </div>

        {/* Stat Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard
            icon={TrendingUp}
            label="Learning Gain"
            value={`${learningGain}%`}
            subtitle="Overall improvement from your baseline assessment"
            color="bg-blue-500"
          />
          <StatCard
            icon={Zap}
            label="Engagement Index"
            value={`${engagementPercent}%`}
            subtitle={engagementPercent >= 60 ? "Great engagement — keep it up!" : "Try to engage more regularly"}
            color={engagementPercent >= 60 ? "bg-emerald-500" : "bg-orange-400"}
          />
          <StatCard
            icon={AlertTriangle}
            label="Risk Score"
            value={`${riskPercent}%`}
            subtitle={riskPercent > 60 ? "High risk — low mastery detected" : "Risk is under control"}
            color={riskPercent > 60 ? "bg-red-500" : "bg-violet-500"}
          />
        </div>

        {/* Main Chart */}
        <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              <h2 className="font-bold text-lg">Mastery Progress Over Time</h2>
              <p className="text-xs text-muted-foreground">
                Each point represents a scored attempt. Milestones are highlighted.
              </p>
            </div>
            {trend !== null && (
              <div className={`flex items-center gap-1 text-sm font-semibold px-3 py-1.5 rounded-full ${trend >= 0 ? "bg-emerald-500/10 text-emerald-500" : "bg-red-500/10 text-red-500"}`}>
                <TrendingUp className={`w-4 h-4 ${trend < 0 ? "rotate-180" : ""}`} />
                {trend >= 0 ? "+" : ""}{trend}% recent trend
              </div>
            )}
          </div>

          {!chartData.length || chartData.length < 2 ? (
            <div className="h-[320px] flex flex-col items-center justify-center gap-3 text-center">
              <BookOpen className="w-12 h-12 text-muted-foreground opacity-40" />
              <p className="text-muted-foreground font-medium">No progress data yet</p>
              <p className="text-xs text-muted-foreground max-w-xs">Complete lessons and quizzes to start seeing your mastery curve here.</p>
            </div>
          ) : (
            <div className="h-[320px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                  <defs>
                    <linearGradient id="progressGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.25} />
                      <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                  <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                  <YAxis domain={[0, 100]} stroke="hsl(var(--muted-foreground))" tick={{ fontSize: 11 }} tickLine={false} axisLine={false} tickFormatter={(v) => `${v}%`} />
                  <Tooltip content={<CustomTooltip />} />
                  {milestones.map((m, i) => (
                    <ReferenceLine key={i} x={chartData[m.index]?.date} stroke={m.color} strokeDasharray="4 4" label={{ value: m.label, position: "top", fontSize: 10, fill: m.color }} />
                  ))}
                  <Area type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={2.5} fill="url(#progressGrad)" dot={{ r: 4, fill: "hsl(var(--primary))", strokeWidth: 0 }} activeDot={{ r: 6, fill: "hsl(var(--primary))" }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          )}
          {/* Milestone legend */}
          {milestones.length > 0 && (
            <div className="flex flex-wrap gap-4 pt-2 border-t border-border">
              {milestones.map((m, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-muted-foreground">
                  <span
                    className="inline-block w-6 h-0.5 border-t-2 border-dashed"
                    style={{ borderColor: m.color }}
                  />
                  {m.label} achieved on {chartData[m.index]?.date}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Radar Map + Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
            <div className="flex items-center gap-2">
              <Hexagon className="w-4 h-4 text-primary" />
              <h2 className="font-bold">Topic Proficiency Map</h2>
            </div>
            {skillTopics.length < 3 ? (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground text-sm italic">Need more topic data to generate map</div>
            ) : (
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={skillTopics}>
                    <PolarGrid stroke="hsl(var(--border))" />
                    <PolarAngleAxis dataKey="topic" tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar name="Mastery" dataKey="value" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.6} />
                    <Tooltip content={<CustomTooltip />} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            )}
            <p className="text-xs text-muted-foreground text-center">
              A multi-dimensional view of your current Python skills.
            </p>
          </div>

          <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
            <div className="flex items-center gap-2">
              <Star className="w-4 h-4 text-primary" />
              <h2 className="font-bold">Mastery Breakdown</h2>
            </div>
            <div className="space-y-3">
              {skillTopics.map((t, i) => (
                <div key={i} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="capitalize truncate max-w-[160px]">{t.topic}</span>
                    <span className="font-semibold text-primary">{t.value}%</span>
                  </div>
                  <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all duration-700" style={{ width: `${t.value}%`, background: t.value >= 80 ? "#22c55e" : t.value >= 50 ? "hsl(var(--primary))" : "#f59e0b" }} />
                  </div>
                </div>
              ))}
              {!skillTopics.length && <p className="text-sm text-muted-foreground text-center py-8">No topic data available yet.</p>}
            </div>
          </div>
        </div>

        {/* Insights Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-20">
          <div className="bg-card border border-border rounded-2xl p-6 space-y-5">
            <div className="flex items-center gap-2">
              <Target className="w-4 h-4 text-primary" />
              <h2 className="font-bold">Performance Insights</h2>
            </div>
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-muted/40 border border-border space-y-1">
                <div className="text-xs text-muted-foreground uppercase tracking-wide font-semibold">Strongest Topic</div>
                <div className="text-lg font-bold">{analytics?.strongestTopic || "—"}</div>
              </div>
              <div className="p-4 rounded-xl bg-muted/40 border border-border space-y-1">
                <div className="text-xs text-muted-foreground uppercase tracking-wide font-semibold">Needs Improvement</div>
                <div className="text-lg font-bold">{analytics?.weakestTopic || "—"}</div>
                {analytics?.weakestTopic && (
                  <p className="text-xs text-muted-foreground mt-1">
                    Focus here to boost your overall mastery score.
                  </p>
                )}
              </div>
              <div className="p-4 rounded-xl bg-muted/40 border border-border space-y-2">
                <div className="text-xs text-muted-foreground uppercase tracking-wide font-semibold">Engagement Meter</div>
                <div className="w-full h-2.5 bg-muted rounded-full overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-700" style={{ width: `${engagementPercent}%`, background: engagementPercent >= 60 ? "#22c55e" : "#f59e0b" }} />
                </div>
                <p className="text-xs text-muted-foreground">
                  {riskPercent > 60
                    ? "⚠️ Low engagement detected. Try completing a lesson today."
                    : "✅ Engagement is healthy. Keep your streak going!"}
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </Layout>
  );
}


import { Layout } from "@/components/Layout";
import { useAuth } from "@/hooks/use-auth";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export function getPresentationScript() {
  return [
    {
      title: "Slide 1 – Title Slide",
      text:
        "This project is called Python Edition: Adaptive and Interactive Learning Assistant. It is an AI-based platform that helps students learn Python in a personalized and interactive way. Our aim is to make Python learning easier, smarter, and more engaging for students.",
    },
    {
      title: "Slide 2 – Problem Statement",
      text:
        "Students learn at different speeds, but most learning platforms give the same content to everyone. Because of this, some students feel bored while others feel confused. There is also less motivation and no proper guidance or fairness in assessments. Our project tries to solve these problems.",
    },
    {
      title: "Slide 3 – Project Overview",
      text:
        "Python Edition is a smart learning platform. It adapts the content based on the learner’s level and performance. It provides lessons, quizzes, coding practice, an AI chatbot, and progress tracking all in one place.",
    },
    {
      title: "Slide 4 – Objectives of the Project",
      text:
        "The main objectives of our project are to understand the learner’s level, recommend suitable content, provide instant help using an AI chatbot, automatically evaluate coding answers, and motivate students using gamification features like badges and streaks.",
    },
    {
      title: "Slide 5 – System Architecture",
      text:
        "The system has three main parts: frontend, backend, and AI layer. The frontend is what the user sees and interacts with. The backend handles data, logic, and user management. The AI layer gives recommendations, chatbot responses, and evaluation.",
    },
    {
      title: "Slide 6 – Methodology",
      text:
        "First, the student logs into the platform and takes a placement quiz. Based on the result, the system identifies strengths and weaknesses. Then, personalized lessons and activities are suggested. The system continuously updates recommendations as the student learns.",
    },
    {
      title: "Slide 7 – AI Chatbot and Auto-Grader",
      text:
        "The AI chatbot helps students by answering Python doubts and explaining errors. The auto-grader runs the student’s code securely and checks it using test cases. It gives instant feedback and hints, which helps students improve their coding skills.",
    },
    {
      title: "Slide 8 – Gamification Features",
      text:
        "To keep students motivated, we added gamification features. Students earn points, badges, and maintain learning streaks. Certificates are provided after completing modules, which encourages consistency.",
    },
    {
      title: "Slide 9 – Assessment Integrity",
      text:
        "To ensure fair exams, we implemented anti-cheating features. The system detects tab switching, disables copy-paste, randomizes questions, and checks code plagiarism. This ensures honesty without using invasive methods like webcams.",
    },
    {
      title: "Slide 10 – Evaluation and Results",
      text:
        "We evaluated our system using learning improvement and engagement metrics. Students showed better understanding after using the platform. Engagement also increased due to personalization and gamification features.",
    },
    {
      title: "Slide 11 – Applications and Impact",
      text:
        "This project can be used in colleges, online learning platforms, and training institutes. It helps self-learners who don’t have access to personal mentors. It also supports fair and effective assessment methods.",
    },
    {
      title: "Slide 12 – Conclusion and Future Scope",
      text:
        "In conclusion, Python Edition is an intelligent and adaptive learning system. In the future, we can extend this platform to other programming languages, add voice-based assistance, and develop a teacher monitoring dashboard.",
    },
  ];
}

export default function Settings() {
  const { user } = useAuth();
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const slides = getPresentationScript();

  return (
    <Layout>
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-display font-bold">Settings</h1>
        </div>

        <Card className="border border-border">
          <CardHeader>
            <CardTitle>Account</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="firstName">First name</Label>
                <Input id="firstName" value={user?.firstName || ""} readOnly />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lastName">Last name</Label>
                <Input id="lastName" value={user?.lastName || ""} readOnly />
              </div>
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" value={user?.email || ""} readOnly />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-border">
          <CardHeader>
            <CardTitle>Preferences</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between rounded-xl border border-border p-4">
              <div>
                <div className="font-medium">Dark mode</div>
                <div className="text-sm text-muted-foreground">Use dark theme across the app</div>
              </div>
              <Switch checked disabled />
            </div>
            <div className="flex items-center justify-between rounded-xl border border-border p-4">
              <div>
                <div className="font-medium">Email notifications</div>
                <div className="text-sm text-muted-foreground">Receive updates about new modules</div>
              </div>
              <Switch checked disabled />
            </div>
          </CardContent>
        </Card>

        <Card className="border border-border">
          <CardHeader>
            <CardTitle>Presentation Script</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {slides.map((s, i) => (
              <div key={i} className="space-y-2">
                <div className="font-medium">{s.title}</div>
                <div className="text-sm text-muted-foreground">{s.text}</div>
                <div className="flex gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => {
                      navigator.clipboard.writeText(`${s.title}\n${s.text}`);
                      setCopiedIndex(i);
                      setTimeout(() => setCopiedIndex(null), 1500);
                    }}
                  >
                    {copiedIndex === i ? "Copied" : "Copy"}
                  </Button>
                </div>
                <Separator />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

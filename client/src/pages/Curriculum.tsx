import { useModules } from "@/hooks/use-modules";
import { useUserProgress } from "@/hooks/use-progress";
import { Layout } from "@/components/Layout";
import { Loader2, Lock, CheckCircle2, ChevronDown, ChevronUp } from "lucide-react";
import { Link, useLocation } from "wouter";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useAuth } from "@/hooks/use-auth";
import { Button } from "@/components/ui/button";

export default function Curriculum() {
  const { data: modules, isLoading: loadingModules, error: modulesError, refetch: refetchModules } = useModules();
  const { data: progress, isLoading: loadingProgress } = useUserProgress();
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const [lockedAlert, setLockedAlert] = useState<{ open: boolean; title: string; type: 'module' | 'lesson' | 'placement' }>({
    open: false,
    title: "",
    type: 'module'
  });
  const [openModules, setOpenModules] = useState<Record<number, boolean>>({ 1: true });
  const { data: quizAttempts, isLoading: loadingQuizAttempts } = useQuery({
    queryKey: ["/api/quiz-attempts"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/quiz-attempts/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return [];
      if (!res.ok) throw new Error("Failed to fetch quiz attempts");
      return res.json();
    },
  });

  const parseModuleLevel = (notes?: string) => {
    if (!notes) return null;
    const match = notes.match(/module:(\d+):level:([A-Za-z]+)/i);
    if (!match) return null;
    return { moduleId: Number(match[1]), level: match[2] };
  };

  const normalizeLevel = (level?: string | null) => {
    if (!level) return "beginner";
    const lower = level.toLowerCase();
    if (lower === "advanced") return "pro";
    return lower;
  };

  const moduleLevels = useMemo(() => {
    const levels: Record<number, string> = {};
    (quizAttempts || []).forEach((attempt: any) => {
      const parsed = parseModuleLevel(attempt?.notes);
      if (parsed && parsed.moduleId) {
        levels[parsed.moduleId] = parsed.level;
      }
    });
    return levels;
  }, [quizAttempts]);

  const allLessons = useMemo(() => {
    if (!modules) return [];
    const fallback = user?.level || "Beginner";
    return (modules as any[]).flatMap((m: any) => {
      const targetLevel = moduleLevels[m.id] || fallback;
      const filtered = (m.lessons || []).filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(targetLevel));
      const lessons = filtered.length > 0 ? filtered : (m.lessons || []);
      return lessons.map((l: any) => ({ ...l, moduleOrder: m.order }));
    })
      .sort((a, b) => {
        if (a.moduleOrder !== b.moduleOrder) return a.moduleOrder - b.moduleOrder;
        return (a.order || 0) - (b.order || 0);
      });
  }, [modules, moduleLevels, user?.level]);

  if (loadingModules || loadingProgress || loadingQuizAttempts) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }
  if (!modules) {
    const status = (modulesError as any)?.status;
    const message = (modulesError as any)?.message || "Unable to load data";
    let title = "Unable to load data";
    let description = "Please refresh the page.";
    let action = (
      <button
        onClick={() => refetchModules()}
        className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
      >
        Retry
      </button>
    );

    if (status === 401) {
      title = "Authentication required";
      description = "Please sign in to continue.";
      action = (
        <button
          onClick={() => (window.location.href = "/login")}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
        >
          Sign in
        </button>
      );
    } else if (status === 403) {
      title = "Placement test required";
      description = "Complete the placement test to unlock your learning path.";
      action = (
        <button
          onClick={() => (window.location.href = "/placement-quiz")}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg"
        >
          Take placement test
        </button>
      );
    }

    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center">
          <h1 className="text-2xl font-bold">{title}</h1>
          <p className="text-muted-foreground mt-2">{description}</p>
          <p className="text-xs text-muted-foreground mt-1">{message}</p>
          <div className="mt-4">{action}</div>
        </div>
      </Layout>
    );
  }

  const isLessonCompleted = (lessonId: number) => {
    return progress?.find(p => p.lessonId === lessonId)?.completed;
  };

  const isModuleCompleted = (moduleId: number) => {
    const module = (modules as any[])?.find(m => m.id === moduleId);
    if (!module || !module.lessons || module.lessons.length === 0) return false;
    const fallback = user?.level || "Beginner";
    const targetLevel = moduleLevels[moduleId] || fallback;
    const filtered = (module.lessons as any[]).filter((l: any) => normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(targetLevel));
    const lessons = filtered.length > 0 ? filtered : (module.lessons as any[]);
    return lessons.every(l => isLessonCompleted(l.id));
  };

  const isModuleLocked = (moduleId: number) => {
    const module = (modules as any[])?.find(m => m.id === moduleId);
    if (!module || module.order === 1) return false;
    
    const previousModule = (modules as any[])?.find(m => m.order === module.order - 1);
    return previousModule ? !isModuleCompleted(previousModule.id) : false;
  };

  const placementCompleted = Boolean(user?.has_taken_quiz || user?.diagnostic_completed);
  const isLessonLocked = (lessonId: number) => {
    // Try to find the lesson in the modules data to see if the API already told us it's unlocked
    const lessonFromModules = modules?.flatMap((m: any) => m.lessons || []).find((l: any) => l.id === lessonId);
    if (lessonFromModules && typeof (lessonFromModules as any).unlocked !== 'undefined') {
      return !(lessonFromModules as any).unlocked;
    }

    const lessonIndex = allLessons.findIndex(l => l.id === lessonId);
    if (lessonIndex <= 0) {
      const firstLesson = allLessons[0];
      if (!firstLesson) return false;
      if (lessonId === firstLesson.id) {
        if (isModuleLocked(firstLesson.moduleId || firstLesson.module_id)) return true;
        return !placementCompleted;
      }
      return false;
    }
    
    const previousLesson = allLessons[lessonIndex - 1];
    return !isLessonCompleted(previousLesson.id);
  };

  const handleLockedClick = (title: string, type: 'module' | 'lesson' | 'placement') => {
    setLockedAlert({ open: true, title, type });
  };

  const toggleModule = (moduleId: number) => {
    setOpenModules(prev => ({ ...prev, [moduleId]: !prev[moduleId] }));
  };

  return (
    <Layout>
      <div className="max-w-5xl mx-auto space-y-12 py-8 px-4">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-display font-bold text-foreground">Python Mastery Path</h1>
          {!placementCompleted ? (
            <div className="max-w-2xl mx-auto bg-card border border-primary/40 rounded-2xl p-4">
              <p className="text-muted-foreground text-sm">
                You must complete the placement test to unlock your personalized Python learning path.
              </p>
              <div className="mt-3">
                <Button onClick={() => setLocation('/placement-quiz')}>Take Placement Test</Button>
              </div>
            </div>
          ) : (
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Unlock new modules and lessons as you master Python.
            </p>
          )}
        </div>

        <div className="bg-card border border-border rounded-2xl p-6">
          <div className="text-sm text-muted-foreground mb-4">Adaptive Learning Path</div>
          <div className="flex flex-wrap items-center gap-3">
            {modules?.map((module, index) => {
              const locked = isModuleLocked(module.id);
              const completed = isModuleCompleted(module.id);
              const level = moduleLevels[module.id] || user?.level || "Beginner";
              return (
                <div key={module.id} className="flex items-center gap-3">
                  <motion.div
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.04 }}
                    className={cn(
                      "px-4 py-2 rounded-full border text-sm font-medium",
                      completed ? "bg-primary text-primary-foreground border-primary" :
                      locked ? "bg-muted text-muted-foreground border-border opacity-60 blur-[0.5px]" :
                      "bg-card text-foreground border-border"
                    )}
                  >
                    {module.title} · {level}
                  </motion.div>
                  {index < (modules?.length || 0) - 1 && (
                    <div className="text-muted-foreground">→</div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        <div className="space-y-16 relative">
          <div className="absolute left-[39px] top-24 bottom-24 w-0.5 bg-border/50 hidden md:block" />

          {modules?.map((module) => {
            const locked = isModuleLocked(module.id);
            const completed = isModuleCompleted(module.id);
            const isOpen = !!openModules[module.id];
            const moduleLevel = moduleLevels[module.id] || user?.level || "Beginner";
            const levelLabel = moduleLevel === "Advanced" ? "Pro" : moduleLevel;
            const moduleQuizCompleted = (quizAttempts || []).some((attempt: any) => attempt?.notes?.includes(`module:${module.id}:level:`));
            const moduleLessons = (module as any).lessons || [];
            const filteredLessons = moduleLessons.filter((l: any) => {
              const target = moduleLevels[module.id] || user?.level || "Beginner";
              return normalizeLevel(l.difficulty || "Beginner") === normalizeLevel(target);
            });
            const visibleLessons = filteredLessons.length > 0 ? filteredLessons : moduleLessons;

            return (
              <div key={module.id} className="relative">
                <div className="flex flex-col md:flex-row gap-8 items-start">
                  <div className={cn(
                    "hidden md:flex shrink-0 w-20 h-20 rounded-full border-4 items-center justify-center font-display text-2xl font-bold z-10 transition-colors",
                    completed ? 'bg-primary border-primary text-primary-foreground' : 
                    locked ? 'bg-muted border-border text-muted-foreground' : 'bg-card border-primary text-primary'
                  )}>
                    {completed ? <CheckCircle2 className="w-10 h-10" /> : module.order}
                  </div>

                  <div className="flex-1 space-y-6 w-full">
                    <Collapsible open={isOpen} onOpenChange={() => toggleModule(module.id)}>
                      <motion.div
                        className={cn(
                          "p-8 rounded-2xl border transition-all duration-300 relative overflow-hidden group",
                          locked ? 'bg-muted/30 border-border opacity-70 grayscale' : 
                          'bg-card border-border hover:border-primary/50 hover:shadow-xl hover:shadow-primary/5',
                          'cursor-pointer'
                        )}
                        onClick={() => toggleModule(module.id)}
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.35 }}
                      >
                        {locked && <Lock className="absolute top-4 right-4 w-6 h-6 text-muted-foreground" />}
                        <div className="absolute top-4 right-4 text-muted-foreground">
                          {isOpen ? <ChevronUp className="w-6 h-6" /> : <ChevronDown className="w-6 h-6" />}
                        </div>
                        
                        <div className="space-y-4 relative z-10">
                          <div className="flex items-center gap-3">
                            <span className={cn(
                              "px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider",
                              completed ? 'bg-primary/20 text-primary' : 'bg-muted text-muted-foreground'
                            )}>
                              Module {module.order}
                            </span>
                            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-muted/70 text-muted-foreground">
                              {levelLabel}
                            </span>
                            {completed && <span className="text-primary text-sm font-medium flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> Completed</span>}
                          </div>
                          
                          <div>
                            <h2 className="text-2xl font-bold text-foreground group-hover:text-primary transition-colors">{module.title}</h2>
                            <p className="text-muted-foreground mt-2 text-lg">{module.description}</p>
                          </div>

                          <div className="flex items-center gap-6 text-sm text-muted-foreground pt-4 border-t border-border/50">
                            <div className="flex items-center gap-2">
                              <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                              {(module as any).lessons?.length || 0} Lessons
                            </div>
                            <div className="flex items-center gap-2">
                              <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                              {levelLabel} track
                            </div>
                          </div>
                        </div>
                      </motion.div>

                      <CollapsibleContent className="pt-4 animate-in fade-in slide-in-from-top-2">
                        <div className="mb-4">
                          <div className={cn(
                            "flex items-center justify-between p-4 rounded-xl border transition-all",
                            locked ? "bg-muted/20 border-border opacity-60" : "bg-card border-border"
                          )}>
                            <div className="space-y-1">
                              <div className="font-medium">Module Quiz</div>
                              <div className="text-sm text-muted-foreground">
                                {moduleQuizCompleted ? `Completed · ${levelLabel} track` : "Take the quiz to personalize this module"}
                              </div>
                            </div>
                            {locked ? (
                              <Button variant="secondary" onClick={() => handleLockedClick(module.title, "module")}>Locked</Button>
                            ) : (
                              <Link href={`/module/${module.id}/quiz`}>
                                <Button>{moduleQuizCompleted ? "Retake Quiz" : "Start Quiz"}</Button>
                              </Link>
                            )}
                          </div>
                          {completed && (
                            <div className="mt-3 flex items-center justify-between p-4 rounded-xl border border-primary/30 bg-primary/5">
                              <div className="text-sm text-primary font-medium">Certificate available</div>
                              <Link href={`/certificate/${module.id}`}>
                                <Button variant="outline">View Certificate</Button>
                              </Link>
                            </div>
                          )}
                        </div>
                        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                          {visibleLessons.sort((a: any,b: any) => (a.order || 0) - (b.order || 0)).map((lesson: any) => {
                            const lLocked = isLessonLocked(lesson.id);
                            const lCompleted = isLessonCompleted(lesson.id);
                            const isFirstLesson = allLessons[0]?.id === lesson.id;
                            const needsPlacement = isFirstLesson && !placementCompleted;

                            return (
                              <div key={lesson.id}>
                                {lLocked ? (
                                  <div 
                                    className="flex items-center gap-4 p-4 rounded-xl border border-border bg-muted/20 opacity-60 cursor-pointer hover:border-primary/30"
                                    onClick={() => needsPlacement ? handleLockedClick("Placement Quiz", "placement") : handleLockedClick(lesson.title, 'lesson')}
                                  >
                                    <Lock className="w-4 h-4 text-muted-foreground shrink-0" />
                                    <span className="font-medium text-muted-foreground text-sm truncate">{lesson.title}</span>
                                  </div>
                                ) : (
                                  <Link href={`/lesson/${lesson.id}`}>
                                    <div className={cn(
                                      "flex items-center justify-between p-4 rounded-xl border transition-all cursor-pointer group hover:border-primary/50",
                                      lCompleted ? 'bg-primary/5 border-primary/30 text-primary' : 'bg-card border-border'
                                    )}>
                                      <div className="flex items-center gap-3 min-w-0">
                                        <div className={cn(
                                          "w-6 h-6 rounded-full flex items-center justify-center font-bold text-[10px] shrink-0",
                                          lCompleted ? 'bg-primary text-primary-foreground' : 'bg-primary/10 text-primary'
                                        )}>
                                          {lCompleted ? <CheckCircle2 className="w-4 h-4" /> : lesson.order}
                                        </div>
                                        <span className={cn("font-medium text-sm truncate", lCompleted ? 'text-primary' : 'text-foreground')}>
                                          {lesson.title}
                                        </span>
                                      </div>
                                    </div>
                                  </Link>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      </CollapsibleContent>
                    </Collapsible>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <AlertDialog open={lockedAlert.open} onOpenChange={(open) => setLockedAlert(prev => ({ ...prev, open }))}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
              <Lock className="w-5 h-5 text-primary" />
              Locked
            </AlertDialogTitle>
            <AlertDialogDescription className="text-base py-4">
              {lockedAlert.type === 'module' 
                ? `Complete all lessons in the previous module to unlock "${lockedAlert.title}".`
                : lockedAlert.type === "placement"
                ? "Complete the placement quiz to unlock your first lesson."
                : `Finish the previous lesson to start "${lockedAlert.title}".`}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            {lockedAlert.type === "placement" ? (
              <>
                <AlertDialogCancel onClick={() => setLockedAlert(prev => ({ ...prev, open: false }))}>Not now</AlertDialogCancel>
                <AlertDialogAction onClick={() => setLocation("/placement-quiz")}>Take placement quiz</AlertDialogAction>
              </>
            ) : (
              <AlertDialogAction onClick={() => setLockedAlert(prev => ({ ...prev, open: false }))}>Got it!</AlertDialogAction>
            )}
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </Layout>
  );
}

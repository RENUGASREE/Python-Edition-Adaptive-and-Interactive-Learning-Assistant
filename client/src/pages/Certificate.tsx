import { Layout } from "@/components/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useAuth } from "@/hooks/use-auth";
import { useModules } from "@/hooks/use-modules";
import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useMemo } from "react";
import { Link, useParams } from "wouter";
import { Loader2 } from "lucide-react";

export default function Certificate() {
  const { id } = useParams();
  const moduleId = Number(id);
  const { user } = useAuth();
  const { data: modules, isLoading: loadingModules } = useModules();
  const { data: certificates, isLoading: loadingCertificates } = useQuery({
    queryKey: ["/api/certificates"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/certificates/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (res.status === 401) return [];
      if (!res.ok) throw new Error("Failed to fetch certificates");
      return res.json();
    },
  });

  const module = useMemo(() => {
    return (modules as any[])?.find((m: any) => m.id === moduleId);
  }, [modules, moduleId]);

  const certificate = useMemo(() => {
    if (!module) return null;
    return (certificates || []).find((c: any) => c.module === module.title);
  }, [certificates, module]);

  if (loadingModules || loadingCertificates) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full py-20">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  if (!moduleId || !module) {
    return (
      <Layout>
        <div className="max-w-xl mx-auto py-16 px-4 text-center">
          <h1 className="text-2xl font-bold">Certificate not found</h1>
          <p className="text-muted-foreground mt-2">Select a module to view its certificate.</p>
          <Link href="/curriculum">
            <Button className="mt-4">Go to curriculum</Button>
          </Link>
        </div>
      </Layout>
    );
  }

  const issueDate = certificate?.issued_at ? new Date(certificate.issued_at).toLocaleDateString() : new Date().toLocaleDateString();

  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12 px-4 space-y-6">
        <Card className="border-2 border-primary/40 shadow-lg">
          <CardContent className="p-10">
            <div className="border-2 border-dashed border-primary/40 p-10 rounded-lg text-center space-y-6">
              <div className="text-sm uppercase tracking-[0.4em] text-muted-foreground">Certificate of Completion</div>
              <div className="text-4xl font-display font-bold text-primary">{module.title}</div>
              <div className="text-muted-foreground text-lg">This certifies that</div>
              <div className="text-3xl font-semibold text-foreground">
                {user?.firstName || user?.email || "Learner"}
              </div>
              <div className="text-muted-foreground text-lg">has successfully completed this module</div>
              <div className="flex items-center justify-center gap-10 pt-6">
                <div className="text-sm text-muted-foreground">
                  Issued on
                  <div className="text-base font-medium text-foreground">{issueDate}</div>
                </div>
                <div className="text-sm text-muted-foreground">
                  Certificate ID
                  <div className="text-base font-medium text-foreground">
                    {certificate?.id || `M${module.id}-${user?.id || "user"}`}
                  </div>
                </div>
              </div>
              {!certificate && (
                <div className="text-sm text-destructive">
                  Complete all lessons in this module to unlock the official certificate.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
        <div className="flex items-center justify-between">
          <Link href="/curriculum">
            <Button variant="outline">Back to curriculum</Button>
          </Link>
          <Button onClick={() => window.print()}>Print certificate</Button>
          <Button onClick={async () => {
            try {
              const accessToken = getAccessToken();
              const response = await fetch(apiUrl(`/api/certificates/${moduleId}/download/`), {
                headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
              });
              if (!response.ok) throw new Error("Failed to download certificate");
              const blob = await response.blob();
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = `certificate_${user?.username}_${moduleId}.pdf`;
              document.body.appendChild(a);
              a.click();
              a.remove();
            } catch (err: any) {
              console.error("Download failed:", err);
            }
          }}>Download PDF</Button>
        </div>
      </div>
    </Layout>
  );
}

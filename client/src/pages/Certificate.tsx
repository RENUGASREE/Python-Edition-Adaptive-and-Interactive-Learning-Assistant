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

  const issueDate = certificate?.issued_at 
    ? new Date(certificate.issued_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) 
    : new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

  return (
    <Layout>
      <div className="max-w-5xl mx-auto py-12 px-4 space-y-8">
        <Card className="border-none shadow-2xl bg-white overflow-hidden relative">
          {/* Certificate Background/Border */}
          <div className="absolute inset-0 border-[16px] border-[#f8f9fa] pointer-events-none" />
          <div className="absolute inset-4 border-2 border-[#1a2b4b] pointer-events-none" />
          <div className="absolute inset-6 border border-[#c5a059] pointer-events-none" />

          <CardContent className="p-16 relative z-10">
            {/* Top Header */}
            <div className="flex justify-between items-start mb-12">
              <div className="text-center flex-1">
                <h3 className="text-[#1a2b4b] font-serif text-2xl font-bold tracking-tight">Python Edition</h3>
              </div>
              <div className="absolute top-12 right-12 bg-[#c5a059] p-0.5 rounded-sm shadow-sm">
                <div className="bg-[#1a2b4b] px-3 py-1 text-[10px] font-bold text-white tracking-wider border border-[#c5a059]">
                  AI VERIFIED LEARNING
                </div>
                <div className="bg-[#c5a059] px-3 py-0.5 text-[9px] font-bold text-[#1a2b4b] text-center">
                  SKILL LEVEL: {user?.level?.toUpperCase() || "PRO"}
                </div>
              </div>
            </div>

            {/* Main Title */}
            <div className="text-center mb-10">
              <h1 className="text-[#1a2b4b] font-serif text-5xl font-extrabold tracking-[0.1em] uppercase">
                Certificate of Achievement
              </h1>
            </div>

            {/* Presentation Text */}
            <div className="text-center mb-8">
              <p className="text-[#4a5568] font-serif text-lg italic">This certification is proudly presented to</p>
            </div>

            {/* Student Name */}
            <div className="text-center mb-12 relative max-w-2xl mx-auto">
              <h2 className="text-[#c5a059] font-serif text-5xl font-bold uppercase tracking-wide py-4">
                {user?.firstName && user?.lastName ? `${user.firstName} ${user.lastName}` : (user?.firstName || user?.email?.split('@')[0] || "Learner")}
              </h2>
              <div className="h-0.5 bg-[#c5a059] w-full mt-2" />
            </div>

            {/* Achievement Description */}
            <div className="text-center mb-6">
              <p className="text-[#4a5568] font-serif text-lg">For successfully mastering the high-fidelity curriculum of</p>
            </div>

            {/* Topic/Module */}
            <div className="text-center mb-16">
              <h3 className="text-[#1a2b4b] font-serif text-3xl font-bold">
                {module.title}
              </h3>
            </div>

            {/* Bottom Section: Signatures, QR, Seal */}
            <div className="flex justify-between items-end mt-12 px-4 pb-4">
              {/* Left: Signature */}
              <div className="w-1/3 text-left pl-4">
                <div className="mb-2">
                  <span className="font-serif text-2xl italic text-[#1a2b4b] border-b border-[#1a2b4b] pb-1 pr-8">
                    Pythonized AI
                  </span>
                </div>
                <div className="text-[10px] font-bold text-[#1a2b4b] uppercase tracking-wider">
                  Platform Director, Python Edition
                </div>
                <div className="text-[10px] text-[#4a5568] mt-4">
                  Issued on: {issueDate}
                </div>
              </div>

              {/* Center: QR Code */}
              <div className="w-1/3 flex flex-col items-center justify-center">
                <div className="bg-white p-2 border border-gray-200 shadow-sm mb-2">
                  <img 
                    src={`https://api.qrserver.com/v1/create-qr-code/?size=80x80&data=https://python-edition.vercel.app/verify/${certificate?.id || 'demo'}`} 
                    alt="Verification QR Code"
                    className="w-16 h-16 opacity-80"
                  />
                </div>
                <div className="text-[8px] text-gray-500 uppercase tracking-widest mb-1">Scan to Verify Certificate</div>
                <div className="text-[9px] font-mono text-gray-600">
                  ID: {certificate?.id || `PY-CERT-${module.id.toString().padStart(3, '0')}-${user?.id?.slice(0,8) || 'VERIFY'}`}
                </div>
              </div>

              {/* Right: Seal */}
              <div className="w-1/3 flex justify-end pr-8">
                <div className="relative w-36 h-36 flex items-center justify-center">
                  {/* Outer Seal Double Circle */}
                  <div className="absolute inset-0 rounded-full border-[3px] border-[#c5a059] shadow-sm" />
                  <div className="absolute inset-1 rounded-full border border-[#c5a059]" />
                  
                  {/* Inner Dark Circle */}
                  <div className="absolute inset-5 rounded-full bg-[#0a192f] flex items-center justify-center shadow-inner border border-[#c5a059]/30">
                    <div className="text-[11px] font-bold text-[#c5a059] tracking-[0.1em] uppercase">Verified</div>
                  </div>

                  {/* Circular Text (SVG) */}
                  <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100">
                    <defs>
                      <path id="circlePath" d="M 50, 50 m -37, 0 a 37,37 0 1,1 74,0 a 37,37 0 1,1 -74,0" fill="none" />
                    </defs>
                    <text className="text-[5.5px] fill-[#c5a059] font-bold uppercase tracking-[0.25em]">
                      <textPath xlinkHref="#circlePath" startOffset="0%">
                        PYTHON EDITION • CERTIFIED • AUTHENTIC • 
                      </textPath>
                    </text>
                  </svg>
                </div>
              </div>
            </div>

            {/* Platform Subtitle */}
            <div className="text-center mt-12 italic text-[#4a5568] font-serif text-sm">
              Python Edition Adaptive Learning Platform
            </div>
          </CardContent>
        </Card>

        <div className="flex items-center justify-center gap-4 no-print">
          <Link href="/curriculum">
            <Button variant="outline" className="px-8">Back to curriculum</Button>
          </Link>
          <Button onClick={() => window.print()} className="px-8">Print certificate</Button>
          <Button 
            className="px-8 bg-[#1a2b4b] hover:bg-[#1a2b4b]/90"
            onClick={async () => {
              try {
                const accessToken = getAccessToken();
                const response = await fetch(apiUrl(`/certificates/${moduleId}/download/`), {
                  headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
                });
                if (!response.ok) throw new Error("Failed to download certificate");
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `certificate_${user?.username || 'learner'}_${moduleId}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
              } catch (err: any) {
                console.error("Download failed:", err);
              }
            }}
          >
            Download PDF
          </Button>
        </div>
      </div>
    </Layout>
  );
}

import { useRoute } from "wouter";
import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, XCircle, Loader2, ShieldCheck, Award } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface VerificationData {
  status: string;
  student: string;
  module: string;
  issued_at: string;
  level: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function VerifyCertificate() {
  const [, params] = useRoute("/verify/:code");
  const code = params?.code;

  const { data, isLoading, isError } = useQuery<VerificationData>({
    queryKey: ["/api/verify/certificate", code],
    queryFn: async () => {
      const res = await fetch(`${API_BASE_URL}/api/verify/certificate/${code}/`);
      if (!res.ok) throw new Error("Certificate not found");
      return res.json();
    },
    enabled: !!code,
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F8F6F2]">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-[#0B1F3A] mx-auto mb-4" />
          <p className="text-[#0B1F3A] font-medium italic">Verifying Authentic Credential...</p>
        </div>
      </div>
    );
  }

  if (isError || data?.status === "not_found") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F8F6F2] p-4">
        <Card className="max-w-md w-full border-2 border-red-200 shadow-xl bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center">
            <XCircle className="h-16 w-16 text-red-500 mx-auto mb-2" />
            <CardTitle className="text-2xl font-bold text-[#0B1F3A]">Invalid Certificate</CardTitle>
          </CardHeader>
          <CardContent className="text-center">
            <p className="text-gray-600">
              The verification code provided does not match any record in our secure database. 
              Please ensure you have scanned the correct QR code.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F8F6F2] p-4 font-serif">
      <Card className="max-w-2xl w-full border-4 border-[#C9A646] shadow-2xl relative overflow-hidden bg-white">
        {/* Luxury Overlay Pattern */}
        <div className="absolute top-0 right-0 p-8 opacity-5">
           <Award className="h-48 w-48 text-[#0B1F3A]" />
        </div>

        <CardHeader className="bg-[#0B1F3A] text-white py-8 text-center">
          <ShieldCheck className="h-12 w-12 text-[#C9A646] mx-auto mb-3" />
          <CardTitle className="text-3xl tracking-widest uppercase">Verified Credential</CardTitle>
          <p className="text-[#C9A646] opacity-90 mt-2 italic">Python Edition Adaptive Learning Platform</p>
        </CardHeader>

        <CardContent className="pt-10 pb-12 px-8 md:px-16 text-center space-y-8">
          <div className="space-y-2">
            <p className="text-sm font-sans tracking-[0.2em] text-gray-400 uppercase">This is to certify that</p>
            <h2 className="text-4xl md:text-5xl font-bold text-[#C9A646] tracking-tight">{data?.student}</h2>
          </div>

          <div className="h-[2px] w-48 bg-[#C9A646]/30 mx-auto" />

          <div className="space-y-3">
            <p className="text-lg text-[#0B1F3A]">has successfully mastered the curriculum of</p>
            <h3 className="text-2xl font-bold text-[#0B1F3A]">{data?.module}</h3>
          </div>

          <div className="flex flex-col md:flex-row justify-center gap-6 pt-6 font-sans">
             <div className="bg-[#F8F6F2] p-4 rounded-lg border border-[#C9A646]/20">
                <p className="text-[10px] text-gray-400 uppercase tracking-widest mb-1">Adaptive Skill Mastery</p>
                <p className="text-xl font-bold text-[#0B1F3A]">{data?.level}</p>
             </div>
             <div className="bg-[#F8F6F2] p-4 rounded-lg border border-[#C9A646]/20">
                <p className="text-[10px] text-gray-400 uppercase tracking-widest mb-1">Official Issue Date</p>
                <p className="text-xl font-bold text-[#0B1F3A]">{data?.issued_at}</p>
             </div>
          </div>

          <div className="pt-8 flex items-center justify-center gap-2 text-green-600 font-sans font-semibold">
            <CheckCircle2 className="h-5 w-5" />
            <span>Digital Authentication Confirmed</span>
          </div>
          
          <p className="text-[10px] text-gray-400 font-sans uppercase tracking-[0.3em]">
             Verification ID: {code?.slice(0, 8).toUpperCase()}...
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

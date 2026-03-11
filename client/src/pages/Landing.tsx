import { Link } from "wouter";
import { BookOpen, BrainCircuit, Code2, ArrowRight } from "lucide-react";
import { Navbar } from "@/components/Navbar";

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#0f1115] text-white selection:bg-primary/30">
      <Navbar />

      {/* Hero */}
      <section className="relative pt-24 pb-32 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-primary/10 blur-[120px] rounded-full pointer-events-none" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            <span className="text-sm font-medium text-accent">New: Interactive AI Tutor</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-display font-bold leading-tight mb-8 bg-gradient-to-br from-white via-white/90 to-white/50 bg-clip-text text-transparent animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
            Master Python with <br />
            <span className="text-primary">Intelligent Feedback</span>
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
            Stop watching videos and start coding. Our AI-powered platform gives you 
            real-time hints, explains concepts, and guides you from "Hello World" to pro.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
            <button 
              onClick={() => window.location.href = "/signin"}
              className="px-8 py-4 bg-primary text-primary-foreground font-bold text-lg rounded-xl hover:bg-primary/90 hover:scale-105 transition-all shadow-lg shadow-primary/25 flex items-center justify-center gap-2"
            >
              Start Learning for Free
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 bg-[#0a0c0f]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={Code2}
              title="Interactive Editor"
              description="Write and execute Python code directly in your browser. No setup required."
            />
            <FeatureCard 
              icon={BrainCircuit}
              title="AI Personal Tutor"
              description="Get stuck? Our AI tutor understands your code and gives personalized hints."
            />
            <FeatureCard 
              icon={BookOpen}
              title="Structured Learning"
              description="Step-by-step curriculum designed by experts to build solid foundations."
            />
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon: Icon, title, description }: { icon: any, title: string, description: string }) {
  return (
    <div className="p-8 rounded-2xl bg-white/5 border border-white/10 hover:border-primary/50 transition-all group">
      <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-6 text-primary group-hover:scale-110 transition-transform">
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-xl font-bold mb-3 font-display">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">{description}</p>
    </div>
  );
}

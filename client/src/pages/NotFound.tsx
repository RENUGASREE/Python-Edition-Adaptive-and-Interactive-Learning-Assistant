import { Link } from "wouter";
import { AlertTriangle } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center bg-background text-center p-4">
      <div className="mb-4 text-accent animate-bounce">
        <AlertTriangle className="h-16 w-16" />
      </div>
      <h1 className="text-4xl font-display font-bold text-foreground mb-4">404 Page Not Found</h1>
      <p className="text-muted-foreground mb-8 text-lg max-w-md">
        Oops! It seems like you've ventured into the unknown void of the internet. 
        Let's get you back to safety.
      </p>
      <Link href="/">
        <button className="px-6 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20">
          Return Home
        </button>
      </Link>
    </div>
  );
}

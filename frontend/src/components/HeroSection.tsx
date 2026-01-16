import { Sparkles } from "lucide-react";

export function HeroSection() {
  return (
    <div className="text-center mb-8">
      <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium mb-4">
        <Sparkles className="h-4 w-4" />
        Powered by AI
      </div>
      <h2 className="text-3xl font-bold tracking-tight mb-3">
        Ask anything about the job market
      </h2>
      <p className="text-muted-foreground max-w-2xl mx-auto">
        Explore 123,000+ LinkedIn job postings using natural language.
        Ask about salaries, companies, industries, and trends.
      </p>
    </div>
  );
}

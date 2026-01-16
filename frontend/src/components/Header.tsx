import { Database } from "lucide-react";

export function Header() {
  return (
    <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
      <div className="container mx-auto px-4 py-4 flex items-center gap-3">
        <div className="flex items-center gap-2">
          <div className="h-9 w-9 rounded-lg bg-primary flex items-center justify-center">
            <Database className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-semibold text-lg leading-tight">Job Market Insights</h1>
            <p className="text-xs text-muted-foreground">AI-powered data exploration</p>
          </div>
        </div>
      </div>
    </header>
  );
}

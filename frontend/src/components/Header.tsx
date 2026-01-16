import { Database } from "lucide-react";

export function Header() {
  return (
    <header className="border-b bg-white/90 backdrop-blur-sm sticky top-0 z-10">
      <div className="container mx-auto px-4 py-3 flex items-center gap-3">
        <div className="flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center shadow-sm">
            <Database className="h-4 w-4 text-white" />
          </div>
          <div>
            <h1 className="font-semibold text-base leading-tight">Job Market Insights</h1>
            <p className="text-xs text-muted-foreground">AI-powered data exploration</p>
          </div>
        </div>
      </div>
    </header>
  );
}

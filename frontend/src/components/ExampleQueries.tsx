import { EXAMPLE_QUERIES } from "@/types";

interface ExampleQueriesProps {
  onExampleClick: (question: string) => void;
}

export function ExampleQueries({ onExampleClick }: ExampleQueriesProps) {
  return (
    <div className="mb-8">
      <p className="text-sm text-muted-foreground mb-3 text-center">Try an example:</p>
      <div className="flex flex-wrap gap-2 justify-center">
        {EXAMPLE_QUERIES.map((example, i) => (
          <button
            key={i}
            onClick={() => onExampleClick(example.question)}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border text-sm hover:bg-slate-50 hover:border-primary/50 transition-colors"
          >
            <span className="text-xs font-medium text-primary">{example.category}</span>
            <span className="text-muted-foreground">·</span>
            <span className="text-slate-700 truncate max-w-[200px]">{example.question}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

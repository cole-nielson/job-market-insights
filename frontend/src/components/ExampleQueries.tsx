import { EXAMPLE_QUERIES } from "@/types";

interface ExampleQueriesProps {
  onExampleClick: (question: string) => void;
}

export function ExampleQueries({ onExampleClick }: ExampleQueriesProps) {
  return (
    <div className="mb-8">
      <p className="text-sm text-muted-foreground mb-4 text-center">
        Try an example query
      </p>
      <div className="flex flex-wrap gap-2 justify-center">
        {EXAMPLE_QUERIES.map((example, i) => (
          <button
            key={i}
            onClick={() => onExampleClick(example.question)}
            className="group inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white border shadow-sm text-sm hover:border-primary/30 hover:shadow-md transition-all"
          >
            <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded">
              {example.category}
            </span>
            <span className="text-slate-600 group-hover:text-slate-900 truncate max-w-[180px]">
              {example.question}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

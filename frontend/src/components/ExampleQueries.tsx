import { motion } from "framer-motion";
import { EXAMPLE_QUERIES } from "@/types";

interface ExampleQueriesProps {
  onExampleClick: (question: string) => void;
}

export function ExampleQueries({ onExampleClick }: ExampleQueriesProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.2 }}
      className="mb-8"
    >
      <p className="text-sm text-muted-foreground mb-4 text-center">
        Try an example query
      </p>
      <div className="flex flex-wrap gap-2 justify-center">
        {EXAMPLE_QUERIES.map((example, i) => (
          <motion.button
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + i * 0.05 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => onExampleClick(example.question)}
            className="group inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white dark:bg-slate-800 border dark:border-slate-700 shadow-sm text-sm hover:border-primary/30 hover:shadow-md transition-all"
          >
            <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded">
              {example.category}
            </span>
            <span className="text-slate-600 dark:text-slate-300 group-hover:text-slate-900 dark:group-hover:text-white truncate max-w-[180px]">
              {example.question}
            </span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}

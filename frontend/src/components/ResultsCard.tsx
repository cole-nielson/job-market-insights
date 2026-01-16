import { useState } from "react";
import { motion } from "framer-motion";
import { Code, ChevronDown, ChevronUp, CheckCircle2, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { DataChart } from "@/components/DataChart";
import type { QueryResponse } from "@/types";

interface ResultsCardProps {
  result: QueryResponse;
  onReset: () => void;
}

export function ResultsCard({ result, onReset }: ResultsCardProps) {
  const [showSql, setShowSql] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="space-y-4"
    >
      <Card className="border-0 shadow-lg overflow-hidden">
        <CardHeader className="pb-3 border-b bg-slate-50/50 dark:bg-slate-800/50">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {result.success ? (
                <CheckCircle2 className="h-4 w-4 text-green-600" />
              ) : (
                <XCircle className="h-4 w-4 text-red-500" />
              )}
              <span className="font-medium">
                {result.success ? "Results" : "Error"}
              </span>
            </div>
            {result.sql && result.success && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSql(!showSql)}
                className="text-xs h-8"
              >
                <Code className="h-3.5 w-3.5 mr-1.5" />
                {showSql ? "Hide SQL" : "View SQL"}
                {showSql ? (
                  <ChevronUp className="h-3.5 w-3.5 ml-1" />
                ) : (
                  <ChevronDown className="h-3.5 w-3.5 ml-1" />
                )}
              </Button>
            )}
          </div>
        </CardHeader>

        {showSql && result.sql && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="px-6 py-4 bg-slate-900 border-b overflow-hidden"
          >
            <code className="text-sm text-slate-100 whitespace-pre-wrap font-mono leading-relaxed">
              {result.sql}
            </code>
          </motion.div>
        )}

        <CardContent className="pt-4">
          <p className="text-[15px] text-slate-700 dark:text-slate-300 whitespace-pre-wrap leading-relaxed">
            {result.response}
          </p>
          {result.visualization &&
            result.visualization.type !== "none" &&
            result.data &&
            result.columns && (
              <DataChart
                data={result.data}
                columns={result.columns}
                visualization={result.visualization}
              />
            )}
        </CardContent>
      </Card>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-center"
      >
        <Button variant="outline" onClick={onReset} className="h-9">
          Ask another question
        </Button>
      </motion.div>
    </motion.div>
  );
}

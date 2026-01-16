import { useState } from "react";
import { Code, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { QueryResponse } from "@/types";

interface ResultsCardProps {
  result: QueryResponse;
  onReset: () => void;
}

export function ResultsCard({ result, onReset }: ResultsCardProps) {
  const [showSql, setShowSql] = useState(false);

  return (
    <>
      <Card className={`border-0 shadow-lg ${result.success ? "" : "border-destructive/50"}`}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {result.success ? (
                <div className="h-2 w-2 rounded-full bg-green-500" />
              ) : (
                <div className="h-2 w-2 rounded-full bg-red-500" />
              )}
              <CardTitle className="text-lg">
                {result.success ? "Results" : "Error"}
              </CardTitle>
            </div>
            {result.sql && result.success && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSql(!showSql)}
                className="text-xs"
              >
                <Code className="h-3.5 w-3.5 mr-1.5" />
                {showSql ? "Hide SQL" : "Show SQL"}
                {showSql ? (
                  <ChevronUp className="h-3.5 w-3.5 ml-1" />
                ) : (
                  <ChevronDown className="h-3.5 w-3.5 ml-1" />
                )}
              </Button>
            )}
          </div>
          {showSql && result.sql && (
            <div className="mt-3 p-3 bg-slate-900 rounded-md overflow-x-auto">
              <code className="text-sm text-slate-100 whitespace-pre-wrap font-mono">
                {result.sql}
              </code>
            </div>
          )}
        </CardHeader>
        <CardContent>
          <CardDescription className="text-base text-foreground whitespace-pre-wrap leading-relaxed">
            {result.response}
          </CardDescription>
        </CardContent>
      </Card>

      <div className="text-center mt-6">
        <Button variant="outline" onClick={onReset}>
          Ask another question
        </Button>
      </div>
    </>
  );
}

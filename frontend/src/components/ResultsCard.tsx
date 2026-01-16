import { useState } from "react";
import { Code, ChevronDown, ChevronUp, CheckCircle2, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import type { QueryResponse } from "@/types";

interface ResultsCardProps {
  result: QueryResponse;
  onReset: () => void;
}

export function ResultsCard({ result, onReset }: ResultsCardProps) {
  const [showSql, setShowSql] = useState(false);

  return (
    <div className="space-y-4">
      <Card className="border-0 shadow-lg overflow-hidden">
        <CardHeader className="pb-3 border-b bg-slate-50/50">
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
          <div className="px-6 py-4 bg-slate-900 border-b">
            <code className="text-sm text-slate-100 whitespace-pre-wrap font-mono leading-relaxed">
              {result.sql}
            </code>
          </div>
        )}

        <CardContent className="pt-4">
          <p className="text-[15px] text-slate-700 whitespace-pre-wrap leading-relaxed">
            {result.response}
          </p>
        </CardContent>
      </Card>

      <div className="text-center">
        <Button variant="outline" onClick={onReset} className="h-9">
          Ask another question
        </Button>
      </div>
    </div>
  );
}

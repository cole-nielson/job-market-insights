import { Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

export function LoadingState() {
  return (
    <Card className="border-0 shadow-lg">
      <CardContent className="py-12 text-center">
        <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary mb-4" />
        <p className="text-muted-foreground">Analyzing your question...</p>
        <p className="text-sm text-muted-foreground/70 mt-1">
          Converting to SQL and querying the database
        </p>
      </CardContent>
    </Card>
  );
}

import { Search, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";

interface SearchBarProps {
  query: string;
  loading: boolean;
  onQueryChange: (query: string) => void;
  onSubmit: (query: string) => void;
}

export function SearchBar({ query, loading, onQueryChange, onSubmit }: SearchBarProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(query);
  };

  return (
    <Card className="mb-6 shadow-lg border-0">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="e.g., What are the top skills for data science roles?"
              value={query}
              onChange={(e) => onQueryChange(e.target.value)}
              className="pl-10 h-12 text-base"
              disabled={loading}
            />
          </div>
          <Button type="submit" size="lg" disabled={loading || !query.trim()}>
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              "Ask"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

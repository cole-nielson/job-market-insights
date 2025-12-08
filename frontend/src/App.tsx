import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Search, Sparkles, Database, Code, Loader2, ChevronDown, ChevronUp } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface QueryResponse {
  success: boolean;
  response: string;
  sql: string;
  error: string | null;
}

interface ExampleQuery {
  question: string;
  category: string;
}

const EXAMPLE_QUERIES: ExampleQuery[] = [
  { question: "What are the most common job titles?", category: "Titles" },
  { question: "What's the average salary for software engineers?", category: "Salary" },
  { question: "Which companies have the most job postings?", category: "Companies" },
  { question: "How many remote jobs are available?", category: "Remote" },
  { question: "What industries have the most job openings?", category: "Industries" },
  { question: "What percentage of jobs are entry-level vs senior?", category: "Experience" },
];

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSql, setShowSql] = useState(false);

  const handleSubmit = async (question: string) => {
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);
    setShowSql(false);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data: QueryResponse = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        response: "Failed to connect to the server. Please try again.",
        sql: "",
        error: String(error),
      });
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (question: string) => {
    setQuery(question);
    handleSubmit(question);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
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

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium mb-4">
            <Sparkles className="h-4 w-4" />
            Powered by AI
          </div>
          <h2 className="text-3xl font-bold tracking-tight mb-3">
            Ask anything about the job market
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Explore 120,000+ LinkedIn job postings using natural language.
            Ask about salaries, companies, industries, and trends.
          </p>
        </div>

        {/* Search Card */}
        <Card className="mb-6 shadow-lg border-0">
          <CardContent className="pt-6">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSubmit(query);
              }}
              className="flex gap-3"
            >
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="e.g., What are the top skills for data science roles?"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
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

        {/* Example Queries */}
        {!result && !loading && (
          <div className="mb-8">
            <p className="text-sm text-muted-foreground mb-3 text-center">Try an example:</p>
            <div className="flex flex-wrap gap-2 justify-center">
              {EXAMPLE_QUERIES.map((example, i) => (
                <button
                  key={i}
                  onClick={() => handleExampleClick(example.question)}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border text-sm hover:bg-slate-50 hover:border-primary/50 transition-colors"
                >
                  <span className="text-xs font-medium text-primary">{example.category}</span>
                  <span className="text-muted-foreground">·</span>
                  <span className="text-slate-700 truncate max-w-[200px]">{example.question}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <Card className="border-0 shadow-lg">
            <CardContent className="py-12 text-center">
              <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary mb-4" />
              <p className="text-muted-foreground">Analyzing your question...</p>
              <p className="text-sm text-muted-foreground/70 mt-1">
                Converting to SQL and querying the database
              </p>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {result && !loading && (
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
        )}

        {/* Ask Another */}
        {result && !loading && (
          <div className="text-center mt-6">
            <Button
              variant="outline"
              onClick={() => {
                setResult(null);
                setQuery("");
              }}
            >
              Ask another question
            </Button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t mt-12 py-6 bg-white">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            Built with FastAPI, React, and OpenAI · Data from LinkedIn Job Postings (2023-2024)
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

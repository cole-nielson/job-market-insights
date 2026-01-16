import { useState } from "react";
import { Header } from "@/components/Header";
import { HeroSection } from "@/components/HeroSection";
import { SearchBar } from "@/components/SearchBar";
import { ExampleQueries } from "@/components/ExampleQueries";
import { LoadingState } from "@/components/LoadingState";
import { ResultsCard } from "@/components/ResultsCard";
import { Footer } from "@/components/Footer";
import { API_URL, type QueryResponse } from "@/types";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (question: string) => {
    if (!question.trim()) return;

    setLoading(true);
    setResult(null);

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

  const handleReset = () => {
    setResult(null);
    setQuery("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <HeroSection />

        <SearchBar
          query={query}
          loading={loading}
          onQueryChange={setQuery}
          onSubmit={handleSubmit}
        />

        {!result && !loading && (
          <ExampleQueries onExampleClick={handleExampleClick} />
        )}

        {loading && <LoadingState />}

        {result && !loading && (
          <ResultsCard result={result} onReset={handleReset} />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;

import { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
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
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== "undefined") {
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    return false;
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

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
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-950 flex flex-col transition-colors duration-300">
      <Header darkMode={darkMode} onToggleDarkMode={() => setDarkMode(!darkMode)} />

      <main className="container mx-auto px-4 py-8 max-w-3xl flex-1">
        <HeroSection />

        <SearchBar
          query={query}
          loading={loading}
          onQueryChange={setQuery}
          onSubmit={handleSubmit}
        />

        <AnimatePresence mode="wait">
          {!result && !loading && (
            <ExampleQueries onExampleClick={handleExampleClick} />
          )}

          {loading && <LoadingState />}

          {result && !loading && (
            <ResultsCard result={result} onReset={handleReset} />
          )}
        </AnimatePresence>
      </main>

      <Footer />
    </div>
  );
}

export default App;

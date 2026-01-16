import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export function HeroSection() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="text-center mb-8"
    >
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.1 }}
        className="inline-flex items-center gap-1.5 bg-primary/10 text-primary px-3 py-1 rounded-full text-xs font-medium mb-4"
      >
        <Sparkles className="h-3.5 w-3.5" />
        Powered by AI
      </motion.div>
      <h2 className="text-2xl sm:text-3xl font-bold tracking-tight mb-2">
        Ask anything about the job market
      </h2>
      <p className="text-muted-foreground text-sm sm:text-base max-w-xl mx-auto">
        Explore 123,000+ LinkedIn job postings using natural language.
        Ask about salaries, companies, industries, and trends.
      </p>
    </motion.div>
  );
}

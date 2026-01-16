import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Check } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const STEPS = [
  "Understanding your question",
  "Generating SQL query",
  "Fetching results",
];

export function LoadingState() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 2200);
    return () => clearInterval(timer);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card className="border-0 shadow-lg">
        <CardContent className="py-8">
          <div className="space-y-3">
            {STEPS.map((step, index) => (
              <motion.div
                key={step}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-3"
              >
                <div className="relative flex items-center justify-center w-5 h-5">
                  <AnimatePresence mode="wait">
                    {index < currentStep ? (
                      <motion.div
                        key="done"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center"
                      >
                        <Check className="w-3 h-3 text-white" />
                      </motion.div>
                    ) : index === currentStep ? (
                      <motion.div
                        key="active"
                        className="w-5 h-5 rounded-full border-2 border-primary border-t-transparent animate-spin"
                      />
                    ) : (
                      <div className="w-5 h-5 rounded-full border-2 border-slate-200 dark:border-slate-700" />
                    )}
                  </AnimatePresence>
                </div>
                <span
                  className={`text-sm ${
                    index <= currentStep
                      ? "text-foreground"
                      : "text-muted-foreground"
                  }`}
                >
                  {step}
                </span>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

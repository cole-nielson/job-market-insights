export interface VisualizationConfig {
  type: "bar" | "pie" | "table" | "none";
  x_key?: string;
  y_key?: string;
  label_key?: string;
}

export interface QueryResponse {
  success: boolean;
  response: string;
  sql: string;
  error: string | null;
  data?: Record<string, unknown>[];
  columns?: string[];
  visualization?: VisualizationConfig;
}

export interface ExampleQuery {
  question: string;
  category: string;
}

export const EXAMPLE_QUERIES: ExampleQuery[] = [
  { question: "What are the most common job titles?", category: "Titles" },
  { question: "What's the average salary for software engineers?", category: "Salary" },
  { question: "Which companies have the most job postings?", category: "Companies" },
  { question: "How many remote jobs are available?", category: "Remote" },
  { question: "What industries have the most job openings?", category: "Industries" },
  { question: "What percentage of jobs are entry-level vs senior?", category: "Experience" },
];

export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

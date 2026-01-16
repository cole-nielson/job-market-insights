import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import type { VisualizationConfig } from "@/types";

interface DataChartProps {
  data: Record<string, unknown>[];
  columns: string[];
  visualization: VisualizationConfig;
}

const COLORS = [
  "#3b82f6", // blue
  "#10b981", // emerald
  "#f59e0b", // amber
  "#ef4444", // red
  "#8b5cf6", // violet
  "#ec4899", // pink
  "#06b6d4", // cyan
  "#f97316", // orange
];

/** Format column name: EXPERIENCE_LEVEL -> Experience Level */
function formatColumnName(col: string): string {
  return col
    .toLowerCase()
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase())
    .replace(/Pct$/, "%")
    .replace(/Id$/, "ID");
}

/** Format value for display */
function formatValue(value: unknown, columnName: string): string {
  if (value === null || value === undefined) return "";

  const colLower = columnName.toLowerCase();

  if (typeof value === "number") {
    // Percentage columns
    if (colLower.includes("pct") || colLower.includes("percent")) {
      return `${value.toFixed(1)}%`;
    }
    // Large numbers get commas
    if (Number.isInteger(value)) {
      return value.toLocaleString();
    }
    // Decimals
    return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }

  return String(value);
}

export function DataChart({ data, columns, visualization }: DataChartProps) {
  if (visualization.type === "none" || !data || data.length === 0) {
    return null;
  }

  if (visualization.type === "bar") {
    return <BarChartView data={data} visualization={visualization} />;
  }

  if (visualization.type === "pie") {
    return <PieChartView data={data} visualization={visualization} />;
  }

  if (visualization.type === "table") {
    return <TableView data={data} columns={columns} />;
  }

  return null;
}

function BarChartView({
  data,
  visualization,
}: {
  data: Record<string, unknown>[];
  visualization: VisualizationConfig;
}) {
  const xKey = visualization.x_key || "";
  const yKey = visualization.y_key || "";

  // Format data for recharts
  const chartData = data.map((row) => ({
    name: String(row[xKey] || ""),
    value: Number(row[yKey]) || 0,
  }));

  return (
    <div className="mt-4 h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{ top: 10, right: 10, left: 10, bottom: 40 }}
        >
          <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={60}
            interval={0}
            tick={{ fontSize: 11, fill: "currentColor" }}
            className="text-slate-600 dark:text-slate-400"
          />
          <YAxis
            tick={{ fontSize: 11, fill: "currentColor" }}
            className="text-slate-600 dark:text-slate-400"
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--tooltip-bg, #fff)",
              border: "1px solid var(--tooltip-border, #e2e8f0)",
              borderRadius: "6px",
              fontSize: "12px",
            }}
            labelStyle={{ fontWeight: 500 }}
            formatter={(value) => (value as number).toLocaleString()}
          />
          <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function PieChartView({
  data,
  visualization,
}: {
  data: Record<string, unknown>[];
  visualization: VisualizationConfig;
}) {
  const labelKey = visualization.label_key || "";
  const yKey = visualization.y_key || "";

  // Format data for recharts
  const chartData = data.map((row) => ({
    name: String(row[labelKey] || ""),
    value: Number(row[yKey]) || 0,
  }));

  return (
    <div className="mt-4 h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={40}
            outerRadius={80}
            paddingAngle={2}
            dataKey="value"
            label={({ name, percent }) =>
              `${name} (${((percent ?? 0) * 100).toFixed(0)}%)`
            }
            labelLine={true}
          >
            {chartData.map((_, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--tooltip-bg, #fff)",
              border: "1px solid var(--tooltip-border, #e2e8f0)",
              borderRadius: "6px",
              fontSize: "12px",
            }}
            formatter={(value) => (value as number).toLocaleString()}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function TableView({
  data,
  columns,
}: {
  data: Record<string, unknown>[];
  columns: string[];
}) {
  // Limit to first 50 rows for display
  const displayData = data.slice(0, 50);
  const hasMore = data.length > 50;

  return (
    <div className="mt-4 overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
      <div className="max-h-64 overflow-auto">
        <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-700">
          <thead className="bg-slate-50 dark:bg-slate-800 sticky top-0">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-3 py-2 text-left text-xs font-medium text-slate-600 dark:text-slate-400 tracking-wider"
                >
                  {formatColumnName(col)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-slate-900 divide-y divide-slate-100 dark:divide-slate-800">
            {displayData.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                {columns.map((col) => (
                  <td
                    key={col}
                    className="px-3 py-2 text-sm text-slate-700 dark:text-slate-300 whitespace-nowrap"
                  >
                    {formatValue(row[col], col)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {hasMore && (
        <div className="px-3 py-2 text-xs text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700">
          Showing first 50 of {data.length.toLocaleString()} rows
        </div>
      )}
    </div>
  );
}

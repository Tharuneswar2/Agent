"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Bot, User as UserIcon, Sparkles } from "lucide-react";
import { MainLayout } from "@/components/MainLayout";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import axios from "axios";

const initialMessages = [
  {
    id: "1",
    role: "assistant" as const,
    content:
      "👋 Hello! I'm your Financial AI Assistant. Ask me about revenue trends, profit growth, or expense breakdowns — and I’ll visualize it instantly!",
    timestamp: new Date(),
  },
];

// ...keep imports and initialMessages as before

export default function ChatPage() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [chartData, setChartData] = useState<any[]>([]);
  const [chartType, setChartType] = useState<string>("bar");
  const [chartBase64, setChartBase64] = useState<string>("");
  const [insight, setInsight] = useState<string>("");
  const [sources, setSources] = useState<any[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current)
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = {
      id: Date.now().toString(),
      role: "user" as const,
      content: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const [queryRes, vizRes] = await Promise.all([
        axios.post("http://localhost:8000/query_router", { query: input }),
        axios.post("http://localhost:8000/visualize_router", { query: input }),
      ]);
      console.log(queryRes.data);
      const aiAnswer =
        queryRes.data?.answer ||
        queryRes.data?.response ||
        "No financial insights found.";
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant" as const,
        content: aiAnswer,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsTyping(false);

      // Save sources for detailed display
      setSources(queryRes.data?.sources || []);

      // Chart handling
      if (vizRes.data?.data?.length > 0) {
        setChartData(vizRes.data.data);
        setChartType(vizRes.data.chart_type || "bar");
        setChartBase64(vizRes.data.chart_base64 || "");
        setInsight(vizRes.data.insight || "");
      } else {
        setChartData([]);
        setChartBase64("");
        setInsight("No visualizable financial data found.");
      }
    } catch (err) {
      console.error("❌ Backend fetch error:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 2).toString(),
          role: "assistant",
          content: "⚠️ Unable to connect to Financial AI backend.",
          timestamp: new Date(),
        },
      ]);
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

  const renderChart = () => {
    if (chartBase64) {
      return (
        <div className="flex justify-center">
          <img
            src={`data:image/png;base64,${chartBase64}`}
            alt="Financial Chart"
            className="rounded-lg shadow-md max-h-[400px]"
          />
        </div>
      );
    }

    if (!chartData.length) {
      return (
        <div className="flex flex-col items-center justify-center h-[400px] text-center">
          <Sparkles className="h-10 w-10 text-muted-foreground mb-3" />
          <h3 className="font-semibold mb-1">Ask a financial question</h3>
          <p className="text-sm text-gray-500">
            e.g., “Revenue trend of Reliance Industries 2025”
          </p>
        </div>
      );
    }

    const keyX = Object.keys(chartData[0])[0];
    const keyY = Object.keys(chartData[0])[1];

    switch (chartType) {
      case "line":
        return (
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={keyX} />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey={keyY}
                stroke="#2563eb"
                strokeWidth={3}
                dot
              />
            </LineChart>
          </ResponsiveContainer>
        );
      case "pie":
        return (
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey={keyY}
                nameKey={keyX}
                outerRadius={120}
                label
              >
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        );
      default:
        return (
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={keyX} />
              <YAxis />
              <Tooltip />
              <Bar dataKey={keyY} fill="#3b82f6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <MainLayout>
      <div className="h-[calc(100vh-4rem)] p-8">
        <div className="grid lg:grid-cols-2 gap-6 h-full">
          {/* Chat Section */}
          <Card className="flex flex-col">
            <div className="border-b p-4">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-yellow-500" /> Financial AI
                Chat
              </h2>
              <p className="text-sm text-muted-foreground">
                Ask about revenue, expenses, or ratios
              </p>
            </div>

            <ScrollArea className="flex-1 p-4" ref={scrollRef}>
              <div className="space-y-4">
                {messages.map((msg) => (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    {msg.role === "assistant" && (
                      <div className="h-8 w-8 flex items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-green-500">
                        <Bot className="h-5 w-5 text-white" />
                      </div>
                    )}
                    <div
                      className={`rounded-lg px-4 py-3 max-w-[80%] ${
                        msg.role === "user"
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted"
                      }`}
                    >
                      <p className="text-sm">{msg.content}</p>
                      <p className="text-xs opacity-70 mt-2">
                        {msg.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </div>
                    {msg.role === "user" && (
                      <div className="h-8 w-8 flex items-center justify-center rounded-lg bg-gradient-to-br from-purple-500 to-pink-500">
                        <UserIcon className="h-5 w-5 text-white" />
                      </div>
                    )}
                  </motion.div>
                ))}

                {isTyping && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex gap-3"
                  >
                    <Bot className="h-6 w-6 text-blue-500 animate-pulse" />
                    <p className="text-sm text-gray-500">Thinking...</p>
                  </motion.div>
                )}
              </div>
            </ScrollArea>

            <div className="border-t p-4 flex gap-2">
              <Input
                placeholder="Ask about financials..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                className="flex-1"
              />
              <Button onClick={handleSend} disabled={isTyping} size="icon">
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </Card>

          {/* Visualization + Data Section */}
          <Card>
            <div className="border-b p-4">
              <h2 className="text-xl font-bold">📊 Financial Insights</h2>
              <p className="text-sm text-muted-foreground mt-1">
                Charts and detailed data
              </p>
            </div>
            <CardContent className="pt-6 space-y-6">
              {renderChart()}
              {insight && (
                <p className="text-center text-gray-600 italic text-sm">
                  💡 {insight}
                </p>
              )}

              {/* Display Sources */}
              {sources.length > 0 && (
                <div className="overflow-x-auto">
                  <h3 className="font-semibold mb-2">Source Data:</h3>
                  <table className="table-auto border-collapse border border-gray-300 w-full text-sm">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="border px-2 py-1">Type</th>
                        <th className="border px-2 py-1">Text</th>
                        <th className="border px-2 py-1">Score</th>
                        <th className="border px-2 py-1">Source</th>
                      </tr>
                    </thead>
                    <tbody>
                      {sources.map((s, i) => (
                        <tr key={i} className="hover:bg-gray-50">
                          <td className="border px-2 py-1">{s.type}</td>
                          <td className="border px-2 py-1">
                            <span
                              dangerouslySetInnerHTML={{ __html: s.text }}
                            />
                          </td>
                          <td className="border px-2 py-1">
                            {s.score?.toFixed(2)}
                          </td>
                          <td className="border px-2 py-1">{s.source}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
}

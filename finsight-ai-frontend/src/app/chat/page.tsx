'use client';

import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, User as UserIcon, Sparkles } from 'lucide-react';
import { MainLayout } from '@/components/MainLayout';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const initialMessages = [
  {
    id: '1',
    role: 'assistant' as const,
    content: 'Hello! I\'m your Financial AI Assistant. Ask me anything about your financial data, such as revenue trends, expense analysis, or profit margins.',
    timestamp: new Date(),
  },
];

const mockChartData = [
  { quarter: 'Q1 2023', revenue: 45000, growth: 8 },
  { quarter: 'Q2 2023', revenue: 52000, growth: 15.5 },
  { quarter: 'Q3 2023', revenue: 58000, growth: 11.5 },
  { quarter: 'Q4 2023', revenue: 67000, growth: 15.5 },
];

export default function ChatPage() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showChart, setShowChart] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: getAIResponse(input),
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
      setIsTyping(false);
      
      // Show chart for revenue-related queries
      if (input.toLowerCase().includes('revenue') || input.toLowerCase().includes('growth')) {
        setShowChart(true);
      }
    }, 1500);
  };

  const getAIResponse = (query: string) => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('revenue') || lowerQuery.includes('growth')) {
      return 'Based on your financial data, Tesla\'s revenue showed strong growth in 2023. Total revenue reached $228K across all quarters, with Q4 showing the highest performance at $67K. The year-over-year growth rate averaged 12.6%, with Q2 and Q4 being particularly strong quarters at 15.5% growth each. I\'ve visualized this trend in the chart on the right.';
    }
    
    if (lowerQuery.includes('profit') || lowerQuery.includes('margin')) {
      return 'Your profit margins have been healthy, averaging around 29% throughout the year. This represents a 2.4% improvement compared to the previous period. The increase is primarily due to operational efficiency improvements and cost optimization in Q2 and Q3.';
    }
    
    if (lowerQuery.includes('expense')) {
      return 'Total expenses for the period were $233K, with a positive trend showing a 3.1% reduction. The breakdown shows: Operations (45%), Marketing (25%), Salaries (20%), and Other (10%). The reduction was primarily achieved through operational efficiency improvements.';
    }
    
    return 'I\'ve analyzed your request. Based on the available financial data, I can provide detailed insights about revenue trends, expense patterns, profit margins, and cash flow. What specific aspect would you like me to explore further?';
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <MainLayout>
      <div className="h-[calc(100vh-4rem)] p-8">
        <div className="h-full grid lg:grid-cols-2 gap-6">
          {/* Chat Panel */}
          <Card className="flex flex-col">
            <div className="border-b p-4">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-yellow-500" />
                Financial AI Chat
              </h2>
              <p className="text-sm text-muted-foreground mt-1">
                Ask questions about your financial data
              </p>
            </div>

            <ScrollArea className="flex-1 p-4" ref={scrollRef}>
              <div className="space-y-4">
                {messages.map((message, index) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`flex gap-3 ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-green-500">
                        <Bot className="h-5 w-5 text-white" />
                      </div>
                    )}
                    
                    <div
                      className={`rounded-lg px-4 py-3 max-w-[80%] ${
                        message.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted'
                      }`}
                    >
                      <p className="text-sm leading-relaxed">{message.content}</p>
                      <p className="text-xs opacity-70 mt-2">
                        {message.timestamp.toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </p>
                    </div>

                    {message.role === 'user' && (
                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-purple-500 to-pink-500">
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
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-green-500">
                      <Bot className="h-5 w-5 text-white" />
                    </div>
                    <div className="rounded-lg px-4 py-3 bg-muted">
                      <div className="flex gap-1">
                        <div className="h-2 w-2 rounded-full bg-foreground/40 animate-bounce" />
                        <div className="h-2 w-2 rounded-full bg-foreground/40 animate-bounce [animation-delay:0.2s]" />
                        <div className="h-2 w-2 rounded-full bg-foreground/40 animate-bounce [animation-delay:0.4s]" />
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>
            </ScrollArea>

            <div className="border-t p-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Ask about revenue, expenses, trends..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="flex-1"
                />
                <Button onClick={handleSend} size="icon">
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card>

          {/* Visualization Panel */}
          <Card>
            <div className="border-b p-4">
              <h2 className="text-xl font-bold">Dynamic Visualization</h2>
              <p className="text-sm text-muted-foreground mt-1">
                Charts update based on your queries
              </p>
            </div>

            <CardContent className="pt-6">
              {showChart ? (
                <div className="space-y-6">
                  <div>
                    <h3 className="font-semibold mb-4">Revenue Growth Trend</h3>
                    <ResponsiveContainer width="100%" height={250}>
                      <LineChart data={mockChartData}>
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                        <XAxis dataKey="quarter" className="text-xs" />
                        <YAxis className="text-xs" />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: 'hsl(var(--card))',
                            border: '1px solid hsl(var(--border))',
                            borderRadius: '8px',
                          }}
                        />
                        <Line
                          type="monotone"
                          dataKey="revenue"
                          stroke="#3b82f6"
                          strokeWidth={3}
                          dot={{ fill: '#3b82f6', r: 5 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  <div>
                    <h3 className="font-semibold mb-4">Growth Rate (%)</h3>
                    <ResponsiveContainer width="100%" height={250}>
                      <BarChart data={mockChartData}>
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                        <XAxis dataKey="quarter" className="text-xs" />
                        <YAxis className="text-xs" />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: 'hsl(var(--card))',
                            border: '1px solid hsl(var(--border))',
                            borderRadius: '8px',
                          }}
                        />
                        <Bar dataKey="growth" fill="#10b981" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-[500px] text-center">
                  <div className="h-20 w-20 rounded-full bg-muted flex items-center justify-center mb-4">
                    <Sparkles className="h-10 w-10 text-muted-foreground" />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">
                    Ask a question to see visualizations
                  </h3>
                  <p className="text-sm text-muted-foreground max-w-sm">
                    Try asking about revenue trends, growth rates, or expense breakdowns
                    to see dynamic charts appear here.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  );
}

'use client';

import { motion } from 'framer-motion';
import { 
  Sparkles, 
  TrendingUp, 
  AlertTriangle, 
  Info, 
  ExternalLink,
  Download,
  FileText
} from 'lucide-react';
import { MainLayout } from '@/components/MainLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

const insights = [
  {
    id: '1',
    title: 'Strong Q4 Performance',
    description: 'Revenue increased by 15.5% in Q4 2023 compared to Q3, marking the strongest quarter of the year. This growth was driven primarily by increased product sales and successful market expansion.',
    type: 'positive',
    impact: 'High',
    source: 'Q4_2024_Balance_Sheet.pdf',
    metrics: ['Revenue: +15.5%', 'Market Share: +3.2%'],
    date: new Date('2024-01-15'),
  },
  {
    id: '2',
    title: 'Operating Efficiency Gains',
    description: 'Operational expenses decreased by 3.1% while maintaining production levels, indicating improved process efficiency and cost management. This contributed to a 2.4% improvement in profit margins.',
    type: 'positive',
    impact: 'Medium',
    source: 'Tesla_Income_Statement_2023.xlsx',
    metrics: ['Expenses: -3.1%', 'Margins: +2.4%'],
    date: new Date('2024-01-14'),
  },
  {
    id: '3',
    title: 'Cash Flow Attention Needed',
    description: 'Days Sales Outstanding (DSO) increased from 45 to 60 days, indicating slower collection from customers. This could impact working capital availability in the coming quarters.',
    type: 'warning',
    impact: 'Medium',
    source: 'Cash_Flow_Analysis.csv',
    metrics: ['DSO: 60 days', 'Change: +15 days'],
    date: new Date('2024-01-14'),
  },
  {
    id: '4',
    title: 'Marketing ROI Improvement',
    description: 'Marketing expenses as a percentage of revenue decreased from 28% to 25%, while customer acquisition increased by 12%. This indicates improved marketing efficiency and better targeting.',
    type: 'positive',
    impact: 'Medium',
    source: 'Q4_2024_Balance_Sheet.pdf',
    metrics: ['CAC: -15%', 'Acquisitions: +12%'],
    date: new Date('2024-01-13'),
  },
  {
    id: '5',
    title: 'Inventory Management Optimization',
    description: 'Inventory turnover ratio improved from 6.2 to 7.8, suggesting better inventory management and reduced holding costs. This frees up capital for other investments.',
    type: 'positive',
    impact: 'Low',
    source: 'Tesla_Income_Statement_2023.xlsx',
    metrics: ['Turnover: 7.8', 'Holding Costs: -12%'],
    date: new Date('2024-01-12'),
  },
  {
    id: '6',
    title: 'Debt-to-Equity Ratio Alert',
    description: 'The debt-to-equity ratio increased from 0.45 to 0.58 over the last quarter. While still within acceptable ranges, continued monitoring is recommended to maintain financial health.',
    type: 'info',
    impact: 'Low',
    source: 'Q4_2024_Balance_Sheet.pdf',
    metrics: ['D/E Ratio: 0.58', 'Change: +0.13'],
    date: new Date('2024-01-11'),
  },
];

export default function InsightsPage() {
  const getTypeIcon = (type: string) => {
    if (type === 'positive') return TrendingUp;
    if (type === 'warning') return AlertTriangle;
    return Info;
  };

  const getTypeColor = (type: string) => {
    if (type === 'positive') return 'text-green-500';
    if (type === 'warning') return 'text-yellow-500';
    return 'text-blue-500';
  };

  const getTypeBadgeColor = (type: string) => {
    if (type === 'positive') return 'bg-green-500/10 text-green-500 hover:bg-green-500/20';
    if (type === 'warning') return 'bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20';
    return 'bg-blue-500/10 text-blue-500 hover:bg-blue-500/20';
  };

  const getImpactBadgeColor = (impact: string) => {
    if (impact === 'High') return 'bg-red-500/10 text-red-500';
    if (impact === 'Medium') return 'bg-orange-500/10 text-orange-500';
    return 'bg-gray-500/10 text-gray-500';
  };

  const handleExport = () => {
    alert('Export functionality would generate a PDF/CSV report of all insights.');
  };

  return (
    <MainLayout>
      <div className="p-8 space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <Sparkles className="h-8 w-8 text-yellow-500" />
              AI-Generated Insights
            </h1>
            <p className="text-muted-foreground mt-1">
              Automated analysis and recommendations based on your financial data
            </p>
          </div>
          <Button onClick={handleExport} className="gap-2">
            <Download className="h-4 w-4" />
            Export Report
          </Button>
        </div>

        {/* Summary Stats */}
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-500/10">
                  <TrendingUp className="h-6 w-6 text-green-500" />
                </div>
                <div>
                  <p className="text-2xl font-bold">4</p>
                  <p className="text-sm text-muted-foreground">Positive Insights</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-500/10">
                  <AlertTriangle className="h-6 w-6 text-yellow-500" />
                </div>
                <div>
                  <p className="text-2xl font-bold">1</p>
                  <p className="text-sm text-muted-foreground">Warnings</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-500/10">
                  <Info className="h-6 w-6 text-blue-500" />
                </div>
                <div>
                  <p className="text-2xl font-bold">1</p>
                  <p className="text-sm text-muted-foreground">Informational</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Insights List */}
        <div className="space-y-4">
          {insights.map((insight, index) => {
            const TypeIcon = getTypeIcon(insight.type);
            const typeColor = getTypeColor(insight.type);
            const typeBadgeColor = getTypeBadgeColor(insight.type);
            const impactBadgeColor = getImpactBadgeColor(insight.impact);

            return (
              <motion.div
                key={insight.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card>
                  <CardHeader>
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-4 flex-1">
                        <div className={`mt-1 p-2 rounded-lg bg-card-foreground/5`}>
                          <TypeIcon className={`h-5 w-5 ${typeColor}`} />
                        </div>
                        <div className="flex-1 space-y-2">
                          <div className="flex items-center gap-2 flex-wrap">
                            <CardTitle className="text-lg">{insight.title}</CardTitle>
                            <Badge className={typeBadgeColor}>
                              {insight.type.charAt(0).toUpperCase() + insight.type.slice(1)}
                            </Badge>
                            <Badge className={impactBadgeColor}>
                              {insight.impact} Impact
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground leading-relaxed">
                            {insight.description}
                          </p>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between flex-wrap gap-4">
                      <div className="flex items-center gap-6">
                        <div>
                          <p className="text-xs text-muted-foreground mb-1">Key Metrics</p>
                          <div className="flex gap-2">
                            {insight.metrics.map((metric, i) => (
                              <Badge key={i} variant="outline" className="text-xs">
                                {metric}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        <div className="h-10 w-px bg-border" />
                        <div>
                          <p className="text-xs text-muted-foreground mb-1">Source</p>
                          <div className="flex items-center gap-1 text-xs">
                            <FileText className="h-3 w-3" />
                            <span className="font-medium">{insight.source}</span>
                          </div>
                        </div>
                        <div className="h-10 w-px bg-border" />
                        <div>
                          <p className="text-xs text-muted-foreground mb-1">Generated</p>
                          <p className="text-xs font-medium">
                            {insight.date.toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <Button variant="outline" size="sm" className="gap-2">
                        <ExternalLink className="h-3 w-3" />
                        View Source
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </div>
    </MainLayout>
  );
}

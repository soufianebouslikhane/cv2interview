'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
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
  LineChart,
  Line,
  Area,
  AreaChart,
  ScatterChart,
  Scatter
} from 'recharts';
import { 
  Briefcase,
  TrendingUp, 
  Target, 
  Award, 
  Users,
  DollarSign,
  Star,
  Download,
  RefreshCw,
  Building,
  GraduationCap,
  Zap
} from 'lucide-react';

interface RoleFrequency {
  role: string;
  frequency: number;
}

interface ConfidenceDistribution {
  high: number;
  medium: number;
  low: number;
}

interface CareerProgressionPattern {
  pattern_type: string;
  frequency: number;
  description: string;
}

interface CareerAnalyticsData {
  total_recommendations: number;
  unique_roles: number;
  average_confidence_score: number;
  top_recommended_roles: RoleFrequency[];
  confidence_distribution: ConfidenceDistribution;
  industry_insights: Record<string, any>;
  career_progression_patterns: CareerProgressionPattern[];
}

interface CareerDashboardProps {
  userId?: string;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C'];

export function CareerDashboard({ userId }: CareerDashboardProps) {
  const [careerData, setCareerData] = useState<CareerAnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchCareerData = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (userId) params.append('user_id', userId);
      
      const response = await fetch(`/api/dashboard/career-analytics?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch career data');
      }
      
      const result = await response.json();
      setCareerData(result.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchCareerData();
  }, [userId]);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchCareerData();
  };

  const handleExport = async () => {
    try {
      const params = new URLSearchParams({
        format: 'json',
        ...(userId && { user_id: userId })
      });
      
      const response = await fetch(`/api/dashboard/export/data?${params}`);
      const data = await response.json();
      
      const blob = new Blob([JSON.stringify(data.data.career_analytics, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `career-analytics-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Career Analytics</h1>
          <div className="flex items-center space-x-2">
            <div className="w-24 h-10 bg-gray-200 rounded animate-pulse" />
            <div className="w-24 h-10 bg-gray-200 rounded animate-pulse" />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i}>
              <CardHeader className="space-y-2">
                <div className="w-24 h-4 bg-gray-200 rounded animate-pulse" />
                <div className="w-16 h-8 bg-gray-200 rounded animate-pulse" />
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="flex items-center text-red-600">
              <Target className="mr-2 h-5 w-5" />
              Error Loading Career Data
            </CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={fetchCareerData} className="w-full">
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!careerData) {
    return null;
  }

  // Process data for visualizations
  const topRolesData = careerData.top_recommended_roles.slice(0, 12);
  
  const confidenceData = [
    { name: 'High (80-100%)', value: careerData.confidence_distribution.high, color: '#00C49F' },
    { name: 'Medium (50-79%)', value: careerData.confidence_distribution.medium, color: '#FFBB28' },
    { name: 'Low (0-49%)', value: careerData.confidence_distribution.low, color: '#FF8042' }
  ];

  const progressionData = careerData.career_progression_patterns.map((pattern, index) => ({
    ...pattern,
    color: COLORS[index % COLORS.length]
  }));

  // Calculate confidence score color
  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.5) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceBadgeVariant = (score: number) => {
    if (score >= 0.8) return 'default';
    if (score >= 0.5) return 'secondary';
    return 'destructive';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Career Analytics</h1>
          <p className="text-muted-foreground">
            Comprehensive analysis of career recommendations and trends
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handleRefresh} disabled={refreshing}>
            <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" size="sm" onClick={handleExport}>
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Recommendations</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{careerData.total_recommendations}</div>
            <p className="text-xs text-muted-foreground">
              Career suggestions generated
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Unique Roles</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{careerData.unique_roles}</div>
            <p className="text-xs text-muted-foreground">
              Different career paths identified
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Confidence</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getConfidenceColor(careerData.average_confidence_score)}`}>
              {(careerData.average_confidence_score * 100).toFixed(1)}%
            </div>
            <Badge variant={getConfidenceBadgeVariant(careerData.average_confidence_score)} className="mt-2">
              {careerData.average_confidence_score >= 0.8 ? 'High' : 
               careerData.average_confidence_score >= 0.5 ? 'Medium' : 'Low'} Confidence
            </Badge>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Career Patterns</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{careerData.career_progression_patterns.length}</div>
            <p className="text-xs text-muted-foreground">
              Progression patterns identified
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts and Analytics */}
      <Tabs defaultValue="roles" className="space-y-4">
        <TabsList>
          <TabsTrigger value="roles">Popular Roles</TabsTrigger>
          <TabsTrigger value="confidence">Confidence Analysis</TabsTrigger>
          <TabsTrigger value="progression">Career Progression</TabsTrigger>
          <TabsTrigger value="insights">Industry Insights</TabsTrigger>
        </TabsList>

        <TabsContent value="roles" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Top Recommended Roles</CardTitle>
                <CardDescription>Most frequently suggested career paths</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={topRolesData} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis 
                      dataKey="role" 
                      type="category" 
                      width={150}
                      tick={{ fontSize: 12 }}
                      tickFormatter={(value) => value.length > 20 ? value.substring(0, 20) + '...' : value}
                    />
                    <Tooltip 
                      formatter={(value, name) => [value, 'Frequency']}
                      labelFormatter={(label) => `Role: ${label}`}
                    />
                    <Bar dataKey="frequency" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Role Distribution</CardTitle>
                <CardDescription>Breakdown of career recommendations</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={topRolesData.slice(0, 8)}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ role, percent }) => `${(percent * 100).toFixed(0)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="frequency"
                    >
                      {topRolesData.slice(0, 8).map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name, props) => [value, props.payload.role]} />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Roles List */}
          <Card>
            <CardHeader>
              <CardTitle>Complete Roles Directory</CardTitle>
              <CardDescription>All recommended career paths with frequency</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {careerData.top_recommended_roles.map((role, index) => (
                  <div key={role.role} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="text-xs">
                        #{index + 1}
                      </Badge>
                      <span className="text-sm font-medium" title={role.role}>
                        {role.role.length > 25 ? role.role.substring(0, 25) + '...' : role.role}
                      </span>
                    </div>
                    <Badge variant="secondary">
                      {role.frequency}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="confidence" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Confidence Score Distribution</CardTitle>
                <CardDescription>How confident our recommendations are</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={confidenceData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {confidenceData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Confidence Metrics</CardTitle>
                <CardDescription>Detailed confidence analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">High Confidence (80-100%)</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={(careerData.confidence_distribution.high / careerData.total_recommendations) * 100} className="w-24" />
                      <Badge variant="default">{careerData.confidence_distribution.high}</Badge>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Medium Confidence (50-79%)</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={(careerData.confidence_distribution.medium / careerData.total_recommendations) * 100} className="w-24" />
                      <Badge variant="secondary">{careerData.confidence_distribution.medium}</Badge>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Low Confidence (0-49%)</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={(careerData.confidence_distribution.low / careerData.total_recommendations) * 100} className="w-24" />
                      <Badge variant="destructive">{careerData.confidence_distribution.low}</Badge>
                    </div>
                  </div>
                </div>

                <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                  <h4 className="font-medium mb-2">Overall Assessment</h4>
                  <p className="text-sm text-muted-foreground">
                    Average confidence score: <span className={`font-bold ${getConfidenceColor(careerData.average_confidence_score)}`}>
                      {(careerData.average_confidence_score * 100).toFixed(1)}%
                    </span>
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    {careerData.average_confidence_score >= 0.8 
                      ? "Excellent recommendation quality with high confidence scores."
                      : careerData.average_confidence_score >= 0.5
                      ? "Good recommendation quality with moderate confidence."
                      : "Recommendations may need more profile data for better accuracy."
                    }
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="progression" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Career Progression Patterns</CardTitle>
                <CardDescription>Common career development paths</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={progressionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="pattern_type" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="frequency" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Progression Insights</CardTitle>
                <CardDescription>Analysis of career development trends</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {careerData.career_progression_patterns.map((pattern, index) => (
                    <div key={pattern.pattern_type} className="p-3 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium">{pattern.pattern_type}</h4>
                        <Badge variant="outline">{pattern.frequency} cases</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{pattern.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Building className="mr-2 h-5 w-5" />
                  Industry Insights
                </CardTitle>
                <CardDescription>Market trends and industry analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">Technology Sector</h4>
                    <p className="text-sm text-blue-700">
                      High demand for software engineers, data scientists, and AI specialists. 
                      Remote work opportunities increasing.
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <h4 className="font-medium text-green-900 mb-2">Healthcare</h4>
                    <p className="text-sm text-green-700">
                      Growing need for healthcare professionals, especially in digital health 
                      and telemedicine roles.
                    </p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <h4 className="font-medium text-purple-900 mb-2">Finance</h4>
                    <p className="text-sm text-purple-700">
                      Fintech roles expanding, with emphasis on blockchain, cryptocurrency, 
                      and digital banking expertise.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="mr-2 h-5 w-5" />
                  Recommendations Summary
                </CardTitle>
                <CardDescription>Key insights and actionable recommendations</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <Award className="h-5 w-5 text-yellow-500 mt-0.5" />
                    <div>
                      <h4 className="font-medium">Top Performing Roles</h4>
                      <p className="text-sm text-muted-foreground">
                        {topRolesData.slice(0, 3).map(role => role.role).join(', ')} show highest recommendation frequency.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <TrendingUp className="h-5 w-5 text-green-500 mt-0.5" />
                    <div>
                      <h4 className="font-medium">Confidence Trends</h4>
                      <p className="text-sm text-muted-foreground">
                        {((careerData.confidence_distribution.high / careerData.total_recommendations) * 100).toFixed(0)}% of recommendations have high confidence scores.
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <Users className="h-5 w-5 text-blue-500 mt-0.5" />
                    <div>
                      <h4 className="font-medium">Career Diversity</h4>
                      <p className="text-sm text-muted-foreground">
                        {careerData.unique_roles} unique roles identified across {careerData.total_recommendations} recommendations.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
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
  TreeMap,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { 
  Search,
  TrendingUp, 
  TrendingDown, 
  Code, 
  Briefcase, 
  Users,
  Target,
  Filter,
  Download,
  RefreshCw,
  Star,
  AlertTriangle
} from 'lucide-react';

interface SkillData {
  skill: string;
  frequency: number;
}

interface SkillAnalyticsData {
  total_unique_skills: number;
  total_skill_mentions: number;
  top_skills: SkillData[];
  skill_categories: Record<string, Record<string, number>>;
  skill_distribution: Record<string, any>;
  trending_skills: string[];
  skill_gaps: string[];
}

interface SkillsDashboardProps {
  userId?: string;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C'];

export function SkillsDashboard({ userId }: SkillsDashboardProps) {
  const [skillsData, setSkillsData] = useState<SkillAnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [refreshing, setRefreshing] = useState(false);

  const fetchSkillsData = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (userId) params.append('user_id', userId);
      
      const response = await fetch(`/api/dashboard/skills-analytics?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch skills data');
      }
      
      const result = await response.json();
      setSkillsData(result.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchSkillsData();
  }, [userId]);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchSkillsData();
  };

  const handleExport = async () => {
    try {
      const params = new URLSearchParams({
        format: 'json',
        ...(userId && { user_id: userId })
      });
      
      const response = await fetch(`/api/dashboard/export/data?${params}`);
      const data = await response.json();
      
      const blob = new Blob([JSON.stringify(data.data.skill_analytics, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `skills-analytics-${new Date().toISOString().split('T')[0]}.json`;
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
          <h1 className="text-3xl font-bold">Skills Analytics</h1>
          <div className="flex items-center space-x-2">
            <div className="w-32 h-10 bg-gray-200 rounded animate-pulse" />
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
              <AlertTriangle className="mr-2 h-5 w-5" />
              Error Loading Skills Data
            </CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={fetchSkillsData} className="w-full">
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!skillsData) {
    return null;
  }

  // Process data for visualizations
  const topSkillsData = skillsData.top_skills.slice(0, 15);
  
  const categoryData = Object.entries(skillsData.skill_categories).map(([category, skills]) => ({
    name: category.replace('_', ' ').toUpperCase(),
    value: Object.values(skills).reduce((sum, count) => sum + count, 0),
    skills: Object.keys(skills).length
  }));

  const skillGapsData = skillsData.skill_gaps.slice(0, 10).map((skill, index) => ({
    skill,
    priority: 10 - index,
    category: 'Gap'
  }));

  const trendingSkillsData = skillsData.trending_skills.slice(0, 10).map((skill, index) => ({
    skill,
    trend: 100 - (index * 5),
    category: 'Trending'
  }));

  // Filter skills based on search and category
  const filteredSkills = topSkillsData.filter(skill => {
    const matchesSearch = skill.skill.toLowerCase().includes(searchTerm.toLowerCase());
    if (selectedCategory === 'all') return matchesSearch;
    
    // Check if skill belongs to selected category
    const categorySkills = skillsData.skill_categories[selectedCategory] || {};
    return matchesSearch && skill.skill.toLowerCase() in Object.keys(categorySkills).map(s => s.toLowerCase());
  });

  const categories = ['all', ...Object.keys(skillsData.skill_categories)];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Skills Analytics</h1>
          <p className="text-muted-foreground">
            Comprehensive analysis of skills across all CVs
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
            <CardTitle className="text-sm font-medium">Total Unique Skills</CardTitle>
            <Code className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{skillsData.total_unique_skills}</div>
            <p className="text-xs text-muted-foreground">
              Across all analyzed CVs
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Mentions</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{skillsData.total_skill_mentions}</div>
            <p className="text-xs text-muted-foreground">
              Total skill occurrences
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Trending Skills</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{skillsData.trending_skills.length}</div>
            <p className="text-xs text-muted-foreground">
              Skills gaining popularity
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Skill Gaps</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{skillsData.skill_gaps.length}</div>
            <p className="text-xs text-muted-foreground">
              Areas for improvement
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filter */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Search className="mr-2 h-5 w-5" />
            Search & Filter Skills
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <Input
                placeholder="Search skills..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full"
              />
            </div>
            <div className="w-full sm:w-48">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {categories.map(category => (
                  <option key={category} value={category}>
                    {category === 'all' ? 'All Categories' : category.replace('_', ' ').toUpperCase()}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Charts and Analytics */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="categories">Categories</TabsTrigger>
          <TabsTrigger value="trends">Trends</TabsTrigger>
          <TabsTrigger value="gaps">Skill Gaps</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Top Skills by Frequency</CardTitle>
                <CardDescription>Most mentioned skills across all CVs</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={filteredSkills.slice(0, 10)} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="skill" type="category" width={100} />
                    <Tooltip />
                    <Bar dataKey="frequency" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Skills by Category</CardTitle>
                <CardDescription>Distribution of skills across categories</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Skills List */}
          <Card>
            <CardHeader>
              <CardTitle>Skills Directory</CardTitle>
              <CardDescription>
                {filteredSkills.length} skills found
                {searchTerm && ` matching "${searchTerm}"`}
                {selectedCategory !== 'all' && ` in ${selectedCategory.replace('_', ' ')}`}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                {filteredSkills.map((skill, index) => (
                  <div key={skill.skill} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="text-xs">
                        #{index + 1}
                      </Badge>
                      <span className="text-sm font-medium">{skill.skill}</span>
                    </div>
                    <Badge variant="secondary">
                      {skill.frequency}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="categories" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(skillsData.skill_categories).map(([category, skills]) => (
              <Card key={category}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    {category.replace('_', ' ').toUpperCase()}
                    <Badge variant="outline">
                      {Object.keys(skills).length} skills
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {Object.entries(skills)
                      .sort(([,a], [,b]) => b - a)
                      .slice(0, 10)
                      .map(([skill, count]) => (
                        <div key={skill} className="flex items-center justify-between">
                          <span className="text-sm">{skill}</span>
                          <div className="flex items-center space-x-2">
                            <Progress value={(count / Math.max(...Object.values(skills))) * 100} className="w-16" />
                            <Badge variant="secondary" className="text-xs">
                              {count}
                            </Badge>
                          </div>
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="trends" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="mr-2 h-5 w-5 text-green-600" />
                  Trending Skills
                </CardTitle>
                <CardDescription>Skills gaining popularity</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {skillsData.trending_skills.slice(0, 10).map((skill, index) => (
                    <div key={skill} className="flex items-center justify-between p-2 border rounded">
                      <div className="flex items-center space-x-2">
                        <Star className="h-4 w-4 text-yellow-500" />
                        <span className="text-sm font-medium">{skill}</span>
                      </div>
                      <Badge variant="outline" className="text-green-600">
                        Trending #{index + 1}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Skill Trend Analysis</CardTitle>
                <CardDescription>Trending vs declining skills comparison</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={trendingSkillsData.slice(0, 8)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="skill" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="trend" fill="#00C49F" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="gaps" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="mr-2 h-5 w-5 text-orange-600" />
                  Identified Skill Gaps
                </CardTitle>
                <CardDescription>Skills that could strengthen profiles</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {skillsData.skill_gaps.slice(0, 10).map((skill, index) => (
                    <div key={skill} className="flex items-center justify-between p-2 border rounded border-orange-200">
                      <div className="flex items-center space-x-2">
                        <AlertTriangle className="h-4 w-4 text-orange-500" />
                        <span className="text-sm font-medium">{skill}</span>
                      </div>
                      <Badge variant="outline" className="text-orange-600">
                        Priority {index + 1}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Skill Gap Priority</CardTitle>
                <CardDescription>Importance ranking of missing skills</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={skillGapsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="skill" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="priority" fill="#FF8042" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

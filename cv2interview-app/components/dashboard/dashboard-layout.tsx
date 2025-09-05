'use client';

import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  Users, 
  FileText, 
  Target,
  Settings,
  Download,
  RefreshCw,
  Activity,
  Briefcase,
  Code,
  Brain
} from 'lucide-react';

import { OverviewDashboard } from './overview-dashboard';
import { SkillsDashboard } from './skills-dashboard';
import { CareerDashboard } from './career-dashboard';

interface DashboardLayoutProps {
  userId?: string;
  userRole?: 'admin' | 'user';
}

export function DashboardLayout({ userId, userRole = 'user' }: DashboardLayoutProps) {
  const [activeTab, setActiveTab] = useState('overview');
  const [systemHealth, setSystemHealth] = useState<{
    status: string;
    health_score: number;
    timestamp: string;
  } | null>(null);

  React.useEffect(() => {
    // Fetch system health on component mount
    fetchSystemHealth();
  }, []);

  const fetchSystemHealth = async () => {
    try {
      const response = await fetch('/api/dashboard/health');
      if (response.ok) {
        const result = await response.json();
        setSystemHealth(result.data);
      }
    } catch (error) {
      console.error('Failed to fetch system health:', error);
    }
  };

  const getHealthStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'text-green-600';
      case 'good': return 'text-blue-600';
      case 'fair': return 'text-yellow-600';
      case 'poor': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getHealthBadgeVariant = (status: string) => {
    switch (status) {
      case 'excellent': return 'default';
      case 'good': return 'secondary';
      case 'fair': return 'outline';
      case 'poor': return 'destructive';
      default: return 'outline';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-blue-600" />
                <h1 className="text-2xl font-bold text-gray-900">CV2Interview Analytics</h1>
              </div>
              {systemHealth && (
                <Badge variant={getHealthBadgeVariant(systemHealth.status)} className="ml-4">
                  <Activity className="h-3 w-3 mr-1" />
                  System {systemHealth.status} ({systemHealth.health_score}%)
                </Badge>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              {userRole === 'admin' && (
                <Button variant="outline" size="sm">
                  <Settings className="h-4 w-4 mr-2" />
                  Admin Settings
                </Button>
              )}
              <Button variant="outline" size="sm" onClick={fetchSystemHealth}>
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          {/* Navigation Tabs */}
          <div className="bg-white rounded-lg border p-1">
            <TabsList className="grid w-full grid-cols-3 lg:grid-cols-4">
              <TabsTrigger value="overview" className="flex items-center space-x-2">
                <BarChart3 className="h-4 w-4" />
                <span className="hidden sm:inline">Overview</span>
              </TabsTrigger>
              <TabsTrigger value="skills" className="flex items-center space-x-2">
                <Code className="h-4 w-4" />
                <span className="hidden sm:inline">Skills</span>
              </TabsTrigger>
              <TabsTrigger value="careers" className="flex items-center space-x-2">
                <Briefcase className="h-4 w-4" />
                <span className="hidden sm:inline">Careers</span>
              </TabsTrigger>
              {userRole === 'admin' && (
                <TabsTrigger value="admin" className="flex items-center space-x-2">
                  <Settings className="h-4 w-4" />
                  <span className="hidden sm:inline">Admin</span>
                </TabsTrigger>
              )}
            </TabsList>
          </div>

          {/* Quick Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Dashboard</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold capitalize">{activeTab}</div>
                <p className="text-xs text-muted-foreground">
                  Current view
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">User Type</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold capitalize">{userRole}</div>
                <p className="text-xs text-muted-foreground">
                  Access level
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Data Scope</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{userId ? 'Personal' : 'Global'}</div>
                <p className="text-xs text-muted-foreground">
                  Analytics scope
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">System Status</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className={`text-2xl font-bold ${systemHealth ? getHealthStatusColor(systemHealth.status) : 'text-gray-600'}`}>
                  {systemHealth ? systemHealth.status : 'Loading...'}
                </div>
                <p className="text-xs text-muted-foreground">
                  {systemHealth ? `${systemHealth.health_score}% health` : 'Checking status...'}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Dashboard Content */}
          <TabsContent value="overview" className="space-y-6">
            <OverviewDashboard userId={userId} />
          </TabsContent>

          <TabsContent value="skills" className="space-y-6">
            <SkillsDashboard userId={userId} />
          </TabsContent>

          <TabsContent value="careers" className="space-y-6">
            <CareerDashboard userId={userId} />
          </TabsContent>

          {userRole === 'admin' && (
            <TabsContent value="admin" className="space-y-6">
              <AdminDashboard />
            </TabsContent>
          )}
        </Tabs>
      </div>
    </div>
  );
}

// Admin Dashboard Component
function AdminDashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          <p className="text-muted-foreground">
            System administration and management tools
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="mr-2 h-5 w-5" />
              User Management
            </CardTitle>
            <CardDescription>Manage user accounts and permissions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                <Users className="mr-2 h-4 w-4" />
                View All Users
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Settings className="mr-2 h-4 w-4" />
                User Permissions
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="mr-2 h-5 w-5" />
              System Monitoring
            </CardTitle>
            <CardDescription>Monitor system performance and health</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                <Activity className="mr-2 h-4 w-4" />
                Performance Metrics
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <TrendingUp className="mr-2 h-4 w-4" />
                Usage Analytics
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Download className="mr-2 h-5 w-5" />
              Data Management
            </CardTitle>
            <CardDescription>Export and backup system data</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                <Download className="mr-2 h-4 w-4" />
                Export All Data
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <FileText className="mr-2 h-4 w-4" />
                Generate Reports
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>System Configuration</CardTitle>
          <CardDescription>Configure system settings and parameters</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-medium">AI Model Settings</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Model Temperature</span>
                  <Badge variant="outline">0.2</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Max Tokens</span>
                  <Badge variant="outline">4000</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Timeout (seconds)</span>
                  <Badge variant="outline">30</Badge>
                </div>
              </div>
            </div>
            
            <div className="space-y-4">
              <h4 className="font-medium">System Limits</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Max File Size</span>
                  <Badge variant="outline">10MB</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Rate Limit</span>
                  <Badge variant="outline">100/hour</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Cache TTL</span>
                  <Badge variant="outline">1 hour</Badge>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

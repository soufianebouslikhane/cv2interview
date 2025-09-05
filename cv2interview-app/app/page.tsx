import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Brain,
  BarChart3,
  Target,
  Zap,
  FileText,
  Users,
  TrendingUp,
  CheckCircle,
  ArrowRight
} from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900">
      {/* Hero Section */}
      <main className="flex flex-col items-center justify-center min-h-screen text-white p-4">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <div className="flex items-center justify-center space-x-3 mb-6">
            <Brain className="h-12 w-12 text-blue-300" />
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
              CV2Interview
            </h1>
          </div>

          <p className="text-xl md:text-2xl max-w-3xl mx-auto opacity-90 leading-relaxed">
            Advanced AI-powered platform for comprehensive CV analysis, career recommendations,
            and interview preparation with real-time analytics.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-8">
            <Link href="/upload" passHref>
              <Button
                className="px-8 py-4 text-lg rounded-full bg-white text-blue-900 hover:bg-gray-100 transition-all duration-300 shadow-lg hover:shadow-xl"
                size="lg"
              >
                <FileText className="mr-2 h-5 w-5" />
                Analyze Your CV
              </Button>
            </Link>

            <Link href="/dashboard" passHref>
              <Button
                variant="outline"
                className="px-8 py-4 text-lg rounded-full border-white text-white hover:bg-white hover:text-blue-900 transition-all duration-300"
                size="lg"
              >
                <BarChart3 className="mr-2 h-5 w-5" />
                View Analytics
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="bg-white/10 rounded-full p-3 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <Brain className="h-8 w-8 text-blue-300" />
              </div>
              <h3 className="font-semibold mb-2">AI-Powered Analysis</h3>
              <p className="text-sm opacity-80">Advanced machine learning for comprehensive CV insights</p>
            </div>

            <div className="text-center">
              <div className="bg-white/10 rounded-full p-3 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <Target className="h-8 w-8 text-blue-300" />
              </div>
              <h3 className="font-semibold mb-2">Career Recommendations</h3>
              <p className="text-sm opacity-80">Personalized career paths with confidence scoring</p>
            </div>

            <div className="text-center">
              <div className="bg-white/10 rounded-full p-3 w-16 h-16 mx-auto mb-3 flex items-center justify-center">
                <BarChart3 className="h-8 w-8 text-blue-300" />
              </div>
              <h3 className="font-semibold mb-2">Real-time Analytics</h3>
              <p className="text-sm opacity-80">Comprehensive dashboards and insights</p>
            </div>
          </div>
        </div>
      </main>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Comprehensive CV Analysis Platform
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need for professional career development and interview preparation
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-2 hover:border-blue-300 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="mr-2 h-6 w-6 text-blue-600" />
                  Smart CV Processing
                </CardTitle>
                <CardDescription>
                  Extract and analyze structured data from any CV format
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    PDF, DOC, DOCX support
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Structured data extraction
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Skills categorization
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-300 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="mr-2 h-6 w-6 text-blue-600" />
                  Career Recommendations
                </CardTitle>
                <CardDescription>
                  AI-powered career path suggestions with confidence scoring
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Personalized role suggestions
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Confidence scoring
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Skill gap analysis
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-300 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="mr-2 h-6 w-6 text-blue-600" />
                  Interview Preparation
                </CardTitle>
                <CardDescription>
                  Generate targeted interview questions based on your profile
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Personalized questions
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Difficulty levels
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Category-based grouping
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-300 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="mr-2 h-6 w-6 text-blue-600" />
                  Analytics Dashboard
                </CardTitle>
                <CardDescription>
                  Comprehensive insights and trend analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Skills analytics
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Career trends
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Performance metrics
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-300 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="mr-2 h-6 w-6 text-blue-600" />
                  Market Insights
                </CardTitle>
                <CardDescription>
                  Industry trends and salary estimates
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Industry demand analysis
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Salary range estimates
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Growth potential assessment
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-300 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="mr-2 h-6 w-6 text-blue-600" />
                  Enterprise Features
                </CardTitle>
                <CardDescription>
                  Advanced features for teams and organizations
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Bulk CV processing
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Team analytics
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    API access
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-16">
            <Link href="/upload">
              <Button size="lg" className="px-8 py-4 text-lg">
                Start Your Analysis
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ProgressBar } from '@/components/progress-bar';
import { FileUploader } from '@/components/file-uploader';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Loader2,
  FileText,
  Brain,
  Target,
  Zap,
  CheckCircle,
  AlertCircle,
  Clock,
  User,
  Briefcase,
  GraduationCap,
  Award,
  TrendingUp,
  BarChart3
} from 'lucide-react';
import { processFile, extractProfile, generateQuestions, getCareerRecommendation } from '@/lib/api';

interface ProcessingStatus {
  stage: 'uploading' | 'extracting' | 'analyzing' | 'generating' | 'complete';
  message: string;
  progress: number;
}

interface ParsedProfile {
  personal_info?: any;
  skills?: any;
  experience?: any;
  education?: any;
  summary?: string;
  total_experience_years?: number;
}

export default function UploadPage() {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [cvText, setCvText] = useState<string | null>(null);
  const [rawProfile, setRawProfile] = useState<string>('');
  const [parsedProfile, setParsedProfile] = useState<ParsedProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatus>({
    stage: 'uploading',
    message: 'Ready to upload',
    progress: 0
  });
  const [selectedAction, setSelectedAction] = useState<'questions' | 'recommendation' | null>(null);
  const router = useRouter();

  const handleFileUpload = async (uploadedFile: File) => {
    setFile(uploadedFile);
    setLoading(true);
    setError(null);

    try {
      // Stage 1: File upload and text extraction
      setProcessingStatus({
        stage: 'uploading',
        message: 'Uploading and processing file...',
        progress: 20
      });

      const textExtracted = await processFile(uploadedFile);
      setCvText(textExtracted);

      // Stage 2: Profile extraction
      setProcessingStatus({
        stage: 'extracting',
        message: 'Extracting profile information...',
        progress: 60
      });

      const profileResponse = await extractProfile(textExtracted);
      const profileOutput = typeof profileResponse === 'string'
        ? profileResponse
        : profileResponse.output || JSON.stringify(profileResponse, null, 2);

      setRawProfile(profileOutput);

      // Try to parse the profile for better display
      try {
        const parsed = JSON.parse(profileOutput);
        setParsedProfile(parsed);
      } catch {
        // If parsing fails, keep the raw profile
      }

      // Stage 3: Complete
      setProcessingStatus({
        stage: 'complete',
        message: 'Profile extracted successfully!',
        progress: 100
      });

      setStep(2);
    } catch (err) {
      console.error('Error during file upload or profile extraction:', err);
      setError('Failed to process file or extract profile. Please try again.');
      setProcessingStatus({
        stage: 'uploading',
        message: 'Ready to upload',
        progress: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateQuestions = async () => {
    if (!cvText) return;
    setSelectedAction('questions');
    setLoading(true);
    setError(null);

    try {
      setProcessingStatus({
        stage: 'generating',
        message: 'Generating personalized interview questions...',
        progress: 30
      });

      const questions = await generateQuestions(cvText);

      setProcessingStatus({
        stage: 'complete',
        message: 'Interview questions generated successfully!',
        progress: 100
      });

      sessionStorage.setItem('interviewQuestions', JSON.stringify(questions));
      sessionStorage.setItem('profileData', rawProfile);

      // Small delay to show completion status
      setTimeout(() => {
        router.push('/results?section=questions');
      }, 1000);

    } catch (err) {
      console.error('Error generating questions:', err);
      setError('Failed to generate interview questions. Please try again.');
      setProcessingStatus({
        stage: 'complete',
        message: 'Profile extracted successfully!',
        progress: 100
      });
    } finally {
      setLoading(false);
      setSelectedAction(null);
    }
  };

  const handleGetCareerRecommendation = async () => {
    if (!cvText) return;
    setSelectedAction('recommendation');
    setLoading(true);
    setError(null);

    try {
      setProcessingStatus({
        stage: 'analyzing',
        message: 'Analyzing your profile for career recommendations...',
        progress: 30
      });

      const recommendation = await getCareerRecommendation(cvText);

      setProcessingStatus({
        stage: 'complete',
        message: 'Career recommendations generated successfully!',
        progress: 100
      });

      sessionStorage.setItem('careerRecommendation', JSON.stringify(recommendation));
      sessionStorage.setItem('profileData', rawProfile);

      // Small delay to show completion status
      setTimeout(() => {
        router.push('/results?section=recommendation');
      }, 1000);

    } catch (err) {
      console.error('Error getting career recommendation:', err);
      setError('Failed to get career recommendation. Please try again.');
      setProcessingStatus({
        stage: 'complete',
        message: 'Profile extracted successfully!',
        progress: 100
      });
    } finally {
      setLoading(false);
      setSelectedAction(null);
    }
  };

  const handleBothActions = async () => {
    if (!cvText) return;
    setLoading(true);
    setError(null);

    try {
      setProcessingStatus({
        stage: 'generating',
        message: 'Generating questions and career recommendations...',
        progress: 20
      });

      // Generate both in parallel
      const [questions, recommendation] = await Promise.all([
        generateQuestions(cvText),
        getCareerRecommendation(cvText)
      ]);

      setProcessingStatus({
        stage: 'complete',
        message: 'All analysis completed successfully!',
        progress: 100
      });

      sessionStorage.setItem('interviewQuestions', JSON.stringify(questions));
      sessionStorage.setItem('careerRecommendation', JSON.stringify(recommendation));
      sessionStorage.setItem('profileData', rawProfile);

      // Small delay to show completion status
      setTimeout(() => {
        router.push('/results?section=all');
      }, 1000);

    } catch (err) {
      console.error('Error generating both analyses:', err);
      setError('Failed to complete analysis. Please try again.');
      setProcessingStatus({
        stage: 'complete',
        message: 'Profile extracted successfully!',
        progress: 100
      });
    } finally {
      setLoading(false);
    }
  };

  const getProgress = () => {
    if (step === 1 && !file) return 0;
    if (step === 1 && file && loading) return 33;
    if (step === 2 && rawProfile) return 66;
    if (step === 3) return 100;
    return 0;
  };

  const getStatusIcon = () => {
    switch (processingStatus.stage) {
      case 'uploading': return <FileText className="h-5 w-5" />;
      case 'extracting': return <Brain className="h-5 w-5" />;
      case 'analyzing': return <Target className="h-5 w-5" />;
      case 'generating': return <Zap className="h-5 w-5" />;
      case 'complete': return <CheckCircle className="h-5 w-5 text-green-600" />;
      default: return <Clock className="h-5 w-5" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Brain className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">CV2Interview</h1>
            </div>
            <Badge variant="outline" className="flex items-center space-x-1">
              {getStatusIcon()}
              <span>{processingStatus.message}</span>
            </Badge>
          </div>
        </div>
      </div>

      <main className="max-w-6xl mx-auto p-4 md:p-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Progress Section */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold">CV Analysis Pipeline</h2>
              <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
                Step {step} of 3
              </Badge>
            </div>
            <ProgressBar currentStep={step} totalSteps={3} progress={getProgress()} />

            {loading && (
              <div className="flex items-center mt-4 text-blue-100">
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                <span>{processingStatus.message}</span>
              </div>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="p-6 border-b">
              <Alert className="border-red-200 bg-red-50">
                <AlertCircle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800">
                  {error}
                </AlertDescription>
              </Alert>
            </div>
          )}

          {/* Step 1: File Upload */}
          {step === 1 && (
            <div className="p-8">
              <div className="text-center mb-8">
                <FileText className="h-16 w-16 text-blue-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Upload Your Resume</h3>
                <p className="text-gray-600 max-w-2xl mx-auto">
                  Upload your CV in PDF, DOC, or DOCX format. Our AI will extract and analyze
                  your professional information to provide personalized insights.
                </p>
              </div>

              <Card className="max-w-2xl mx-auto border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors">
                <CardContent className="p-8">
                  <FileUploader onFileUpload={handleFileUpload} loading={loading} />
                </CardContent>
              </Card>

              {/* Features Preview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div className="text-center">
                  <div className="bg-blue-100 rounded-full p-3 w-12 h-12 mx-auto mb-3 flex items-center justify-center">
                    <Brain className="h-6 w-6 text-blue-600" />
                  </div>
                  <h4 className="font-semibold mb-2">Smart Analysis</h4>
                  <p className="text-sm text-gray-600">AI-powered extraction of skills, experience, and education</p>
                </div>

                <div className="text-center">
                  <div className="bg-green-100 rounded-full p-3 w-12 h-12 mx-auto mb-3 flex items-center justify-center">
                    <Target className="h-6 w-6 text-green-600" />
                  </div>
                  <h4 className="font-semibold mb-2">Career Insights</h4>
                  <p className="text-sm text-gray-600">Personalized role recommendations with confidence scores</p>
                </div>

                <div className="text-center">
                  <div className="bg-purple-100 rounded-full p-3 w-12 h-12 mx-auto mb-3 flex items-center justify-center">
                    <Zap className="h-6 w-6 text-purple-600" />
                  </div>
                  <h4 className="font-semibold mb-2">Interview Prep</h4>
                  <p className="text-sm text-gray-600">Tailored interview questions based on your profile</p>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Profile Review and Actions */}
          {step === 2 && (
            <div className="p-8">
              <div className="text-center mb-8">
                <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Profile Extracted Successfully!</h3>
                <p className="text-gray-600 max-w-2xl mx-auto">
                  Your CV has been analyzed. Review the extracted information and choose your next step.
                </p>
              </div>

              <Tabs defaultValue="preview" className="max-w-4xl mx-auto">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="preview">Profile Preview</TabsTrigger>
                  <TabsTrigger value="structured">Structured Data</TabsTrigger>
                </TabsList>

                <TabsContent value="preview" className="mt-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <User className="mr-2 h-5 w-5" />
                        Extracted Profile Information
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      {parsedProfile ? (
                        <div className="space-y-6">
                          {/* Personal Info */}
                          {parsedProfile.personal_info && (
                            <div>
                              <h4 className="font-semibold flex items-center mb-3">
                                <User className="mr-2 h-4 w-4" />
                                Personal Information
                              </h4>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                {Object.entries(parsedProfile.personal_info).map(([key, value]) => (
                                  <div key={key} className="flex justify-between">
                                    <span className="font-medium capitalize">{key.replace('_', ' ')}:</span>
                                    <span className="text-gray-600">{String(value)}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Skills */}
                          {parsedProfile.skills && (
                            <div>
                              <h4 className="font-semibold flex items-center mb-3">
                                <Brain className="mr-2 h-4 w-4" />
                                Skills
                              </h4>
                              <div className="space-y-3">
                                {Object.entries(parsedProfile.skills).map(([category, skills]) => (
                                  <div key={category}>
                                    <h5 className="text-sm font-medium text-gray-700 mb-2 capitalize">
                                      {category.replace('_', ' ')}
                                    </h5>
                                    <div className="flex flex-wrap gap-2">
                                      {Array.isArray(skills) && skills.map((skill, index) => (
                                        <Badge key={index} variant="secondary" className="text-xs">
                                          {skill}
                                        </Badge>
                                      ))}
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Experience */}
                          {parsedProfile.experience && Array.isArray(parsedProfile.experience) && (
                            <div>
                              <h4 className="font-semibold flex items-center mb-3">
                                <Briefcase className="mr-2 h-4 w-4" />
                                Work Experience
                              </h4>
                              <div className="space-y-4">
                                {parsedProfile.experience.map((exp, index) => (
                                  <div key={index} className="border-l-2 border-blue-200 pl-4">
                                    <h5 className="font-medium">{exp.position}</h5>
                                    <p className="text-sm text-gray-600">{exp.company}</p>
                                    <p className="text-xs text-gray-500">{exp.duration}</p>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Education */}
                          {parsedProfile.education && Array.isArray(parsedProfile.education) && (
                            <div>
                              <h4 className="font-semibold flex items-center mb-3">
                                <GraduationCap className="mr-2 h-4 w-4" />
                                Education
                              </h4>
                              <div className="space-y-3">
                                {parsedProfile.education.map((edu, index) => (
                                  <div key={index} className="border-l-2 border-green-200 pl-4">
                                    <h5 className="font-medium">{edu.degree}</h5>
                                    <p className="text-sm text-gray-600">{edu.institution}</p>
                                    <p className="text-xs text-gray-500">{edu.graduation_year}</p>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="bg-gray-50 rounded-lg p-4">
                          <pre className="text-sm whitespace-pre-wrap font-mono overflow-auto max-h-96">
                            {rawProfile}
                          </pre>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </TabsContent>

                <TabsContent value="structured" className="mt-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Raw Extracted Data</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="bg-gray-50 rounded-lg p-4">
                        <pre className="text-sm whitespace-pre-wrap font-mono overflow-auto max-h-96">
                          {rawProfile}
                        </pre>
                      </div>
                    </CardContent>
                  </Card>
                </TabsContent>
              </Tabs>

              {/* Action Buttons */}
              <div className="mt-8 max-w-4xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <Card className="border-2 hover:border-blue-400 transition-colors cursor-pointer">
                    <CardContent className="p-6 text-center">
                      <Zap className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                      <h4 className="font-semibold mb-2">Interview Questions</h4>
                      <p className="text-sm text-gray-600 mb-4">
                        Generate personalized interview questions based on your profile
                      </p>
                      <Button
                        onClick={handleGenerateQuestions}
                        disabled={loading}
                        className="w-full"
                        variant={selectedAction === 'questions' ? 'default' : 'outline'}
                      >
                        {loading && selectedAction === 'questions' ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <Zap className="mr-2 h-4 w-4" />
                        )}
                        Generate Questions
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-green-400 transition-colors cursor-pointer">
                    <CardContent className="p-6 text-center">
                      <Target className="h-12 w-12 text-green-600 mx-auto mb-4" />
                      <h4 className="font-semibold mb-2">Career Recommendations</h4>
                      <p className="text-sm text-gray-600 mb-4">
                        Get AI-powered career suggestions with confidence scores
                      </p>
                      <Button
                        onClick={handleGetCareerRecommendation}
                        disabled={loading}
                        className="w-full"
                        variant={selectedAction === 'recommendation' ? 'default' : 'outline'}
                      >
                        {loading && selectedAction === 'recommendation' ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <Target className="mr-2 h-4 w-4" />
                        )}
                        Get Recommendations
                      </Button>
                    </CardContent>
                  </Card>

                  <Card className="border-2 hover:border-indigo-400 transition-colors cursor-pointer">
                    <CardContent className="p-6 text-center">
                      <TrendingUp className="h-12 w-12 text-indigo-600 mx-auto mb-4" />
                      <h4 className="font-semibold mb-2">Complete Analysis</h4>
                      <p className="text-sm text-gray-600 mb-4">
                        Generate both interview questions and career recommendations
                      </p>
                      <Button
                        onClick={handleBothActions}
                        disabled={loading}
                        className="w-full bg-indigo-600 hover:bg-indigo-700"
                      >
                        {loading && !selectedAction ? (
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        ) : (
                          <BarChart3 className="mr-2 h-4 w-4" />
                        )}
                        Complete Analysis
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

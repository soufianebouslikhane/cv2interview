'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { ProgressBar } from '@/components/progress-bar';
import { ProfileDisplay } from '@/components/profile-display';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ProfileData } from '../upload/page';

export default function ResultsPage() {
  const [interviewQuestions, setInterviewQuestions] = useState<string[]>([]);
  const [careerRecommendation, setCareerRecommendation] = useState<string | null>(null);
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();
  const section = searchParams.get('section');

  useEffect(() => {
    // Récupérer les données stockées en sessionStorage
    const storedQuestionsRaw = sessionStorage.getItem('interviewQuestions');
    if (storedQuestionsRaw) {
      try {
        // Le backend renvoie un objet JSON avec clé 'output' contenant un string avec les questions
        const parsed = JSON.parse(storedQuestionsRaw);
        let questionsText = '';

        // Si c’est un objet avec clé 'output', récupérer ce texte
        if (typeof parsed === 'object' && parsed !== null && 'output' in parsed) {
          questionsText = parsed.output as string;
        } else if (typeof parsed === 'string') {
          questionsText = parsed;
        }

        // Séparer les questions par retour à la ligne, en nettoyant les lignes vides
        const questionsArray = questionsText
          .split('\n')
          .map((q) => q.trim())
          .filter((q) => q.length > 0);

        setInterviewQuestions(questionsArray);
      } catch {
        // Si erreur JSON.parse, utiliser la chaîne brute
        setInterviewQuestions([storedQuestionsRaw]);
      }
    }

    const storedRecommendationRaw = sessionStorage.getItem('careerRecommendation');
    if (storedRecommendationRaw) {
      try {
        const parsed = JSON.parse(storedRecommendationRaw);
        let recommendationText = '';

        if (typeof parsed === 'object' && parsed !== null && 'output' in parsed) {
          recommendationText = parsed.output as string;
        } else if (typeof parsed === 'string') {
          recommendationText = parsed;
        }
        setCareerRecommendation(recommendationText);
      } catch {
        setCareerRecommendation(storedRecommendationRaw);
      }
    }

    const storedProfileRaw = sessionStorage.getItem('profileData');
    if (storedProfileRaw) {
      try {
        setProfile(JSON.parse(storedProfileRaw));
      } catch {
        setProfile(null);
      }
    }
  }, []);

  const handleRestart = () => {
    sessionStorage.clear();
    router.push('/upload');
  };

  return (
    <main className="min-h-screen bg-soft-gray p-4 md:p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6 md:p-8">
        <h1 className="text-3xl font-bold text-navy-blue mb-6 text-center">CV2Interview Results</h1>

        <ProgressBar currentStep={3} totalSteps={3} progress={100} />

        {profile && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle className="text-2xl text-navy-blue text-center">Your Professional Profile</CardTitle>
            </CardHeader>
            <CardContent className="p-6 whitespace-pre-wrap font-mono bg-gray-50 rounded">
              <ProfileDisplay profile={profile} />
            </CardContent>
          </Card>
        )}

        {section === 'questions' && interviewQuestions.length > 0 && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle className="text-2xl text-navy-blue text-center">Personalized Interview Questions</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <ol className="list-decimal list-inside space-y-2 text-gray-800">
                {interviewQuestions.map((question, index) => (
                  <li key={index}>{question}</li>
                ))}
              </ol>
            </CardContent>
          </Card>
        )}

        {section === 'recommendation' && careerRecommendation && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle className="text-2xl text-navy-blue text-center">Career Path Recommendation</CardTitle>
            </CardHeader>
            <CardContent className="p-6 whitespace-pre-wrap font-mono bg-gray-50 rounded">
              {careerRecommendation}
            </CardContent>
          </Card>
        )}

        <div className="flex justify-center mt-8">
          <Button
            onClick={handleRestart}
            className="bg-accent-blue hover:bg-blue-700 text-white rounded-md px-6 py-3 transition-colors duration-300 shadow-md"
          >
            Upload Another CV
          </Button>
        </div>
      </div>
    </main>
  );
}

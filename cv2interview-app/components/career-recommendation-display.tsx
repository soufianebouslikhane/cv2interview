import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Lightbulb, TrendingUp } from 'lucide-react';

interface CareerRecommendationDisplayProps {
  recommendation: string;
}

export function CareerRecommendationDisplay({ recommendation }: CareerRecommendationDisplayProps) {
  // Simple parsing to highlight the suggested role if it's clearly stated
  const highlightRole = (text: string) => {
    const match = text.match(/(suggested role|recommended career path|ideal position):\s*([A-Za-z\s-]+)/i);
    if (match && match[2]) {
      const role = match[2].trim();
      return (
        <>
          {text.split(new RegExp(`(${role})`, 'i')).map((part, index) =>
            part.toLowerCase() === role.toLowerCase() ? (
              <span key={index} className="font-bold text-accent-blue">
                {part}
              </span>
            ) : (
              part
            )
          )}
        </>
      );
    }
    return text;
  };

  return (
    <Card className="shadow-md">
      <CardHeader>
        <CardTitle className="flex items-center text-navy-blue">
          <TrendingUp className="mr-2 h-5 w-5 text-accent-blue" /> Your Career Recommendation
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="bg-soft-gray border border-gray-200 rounded-lg p-6 text-gray-800 leading-relaxed text-lg">
          <p className="mb-4 flex items-center text-navy-blue font-semibold">
            <Lightbulb className="mr-2 h-5 w-5 text-accent-blue" />
            Based on your profile, here's a personalized career path recommendation:
          </p>
          <p className="whitespace-pre-wrap">{highlightRole(recommendation)}</p>
        </div>
      </CardContent>
    </Card>
  );
}

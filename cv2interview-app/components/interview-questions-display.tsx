'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Copy, Download } from 'lucide-react';
import { toast } from 'react-hot-toast'; // Assuming you have a toast notification system

interface InterviewQuestionsDisplayProps {
  questions: string[];
}

export function InterviewQuestionsDisplay({ questions }: InterviewQuestionsDisplayProps) {
  const questionsText = questions.map((q, i) => `${i + 1}. ${q}`).join('\n\n');

  const handleCopy = () => {
    navigator.clipboard.writeText(questionsText);
    // toast.success('Questions copied to clipboard!'); // Uncomment if you have toast setup
    alert('Questions copied to clipboard!');
  };

  const handleDownload = () => {
    const blob = new Blob([questionsText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'interview_questions.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    // toast.success('Questions downloaded!'); // Uncomment if you have toast setup
    alert('Questions downloaded!');
  };

  return (
    <Card className="shadow-md">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-navy-blue">Your Interview Questions</CardTitle>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={handleCopy} className="text-navy-blue hover:bg-soft-gray">
            <Copy className="h-4 w-4 mr-2" /> Copy
          </Button>
          <Button variant="outline" size="sm" onClick={handleDownload} className="text-navy-blue hover:bg-soft-gray">
            <Download className="h-4 w-4 mr-2" /> Download
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {questions.length > 0 ? (
          <ul className="list-decimal pl-5 space-y-3">
            {questions.map((question, index) => (
              <li
                key={index}
                className="text-gray-800 text-base leading-relaxed p-2 rounded-md bg-gray-50 hover:bg-gray-100 transition-colors duration-200"
                style={{ animation: `fadeInUp 0.5s ease-out ${index * 0.1}s forwards`, opacity: 0 }}
              >
                {question}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500 text-center py-4">No interview questions generated yet.</p>
        )}
      </CardContent>
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </Card>
  );
}

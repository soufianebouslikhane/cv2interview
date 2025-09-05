import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  currentStep: number;
  totalSteps: number;
  progress: number; // 0-100
}

export function ProgressBar({ currentStep, totalSteps, progress }: ProgressBarProps) {
  const steps = ['Upload', 'Profile Preview', 'Results'];

  return (
    <div className="w-full mb-8">
      <div className="flex justify-between text-sm font-medium text-gray-600 mb-2">
        {steps.map((stepName, index) => (
          <span
            key={stepName}
            className={cn(
              'transition-colors duration-300',
              currentStep >= index + 1 ? 'text-navy-blue' : 'text-gray-400'
            )}
          >
            {index + 1}. {stepName}
          </span>
        ))}
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
        <div
          className="bg-accent-blue h-2.5 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
}

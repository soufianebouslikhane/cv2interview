import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Briefcase, GraduationCap, Lightbulb } from 'lucide-react';
import { ProfileData } from '@/app/upload/page';

interface ProfileDisplayProps {
  profile?: ProfileData;
}

export function ProfileDisplay({ profile: initialProfile }: ProfileDisplayProps) {
  const [profile, setProfile] = useState<ProfileData | null>(initialProfile || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!profile) {
      setLoading(true);
      setError(null);
      fetch('/api/profile') // Change this endpoint to your backend's profile endpoint
        .then(async (res) => {
          if (!res.ok) throw new Error(await res.text());
          return res.json();
        })
        .then((data) => setProfile(data))
        .catch((err) => setError("Failed to load profile"))
        .finally(() => setLoading(false));
    }
  }, [profile]);

  if (loading) {
    return <div className="text-center text-gray-500 py-8">Loading profile...</div>;
  }
  if (error) {
    return <div className="text-center text-red-500 py-8">{error}</div>;
  }

  // If still no profile, show nothing
  if (!profile) return null;

  return (
    <div className="space-y-6">
      {/* Skills Section */}
      <Card className="shadow-sm hover:shadow-md transition-shadow duration-300">
        <CardHeader>
          <CardTitle className="flex items-center text-navy-blue">
            <Lightbulb className="mr-2 h-5 w-5 text-accent-blue" /> Skills
          </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {Array.isArray(profile.skills) && profile.skills.length > 0 ? (
            profile.skills.map((skill, index) => (
              <Badge key={index} className="bg-accent-blue text-white px-3 py-1 rounded-full text-sm">
                {skill}
              </Badge>
            ))
          ) : (
            <p className="text-gray-500">No skills extracted.</p>
          )}
        </CardContent>
      </Card>

      {/* Experience Section */}
      <Card className="shadow-sm hover:shadow-md transition-shadow duration-300">
        <CardHeader>
          <CardTitle className="flex items-center text-navy-blue">
            <Briefcase className="mr-2 h-5 w-5 text-accent-blue" /> Experience
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.isArray(profile.experience) && profile.experience.length > 0 ? (
            profile.experience.map((exp, index) => (
              <div key={index} className="border-b pb-3 last:border-b-0 last:pb-0">
                <h3 className="font-semibold text-lg text-navy-blue">{exp.title}</h3>
                <p className="text-gray-700">{exp.company} | {exp.duration}</p>
                <p className="text-gray-600 text-sm mt-1">{exp.description}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No experience extracted.</p>
          )}
        </CardContent>
      </Card>

      {/* Education Section */}
      <Card className="shadow-sm hover:shadow-md transition-shadow duration-300">
        <CardHeader>
          <CardTitle className="flex items-center text-navy-blue">
            <GraduationCap className="mr-2 h-5 w-5 text-accent-blue" /> Education
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.isArray(profile.education) && profile.education.length > 0 ? (
            profile.education.map((edu, index) => (
              <div key={index} className="border-b pb-3 last:border-b-0 last:pb-0">
                <h3 className="font-semibold text-lg text-navy-blue">{edu.degree}</h3>
                <p className="text-gray-700">{edu.institution} | {edu.year}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">No education extracted.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

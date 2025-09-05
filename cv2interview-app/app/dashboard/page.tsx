'use client';

import React from 'react';
import { DashboardLayout } from '@/components/dashboard/dashboard-layout';

export default function DashboardPage() {
  // In a real application, you would get these from authentication context
  const userId = undefined; // Set to user ID for personal analytics, undefined for global
  const userRole = 'user'; // 'admin' or 'user'

  return (
    <DashboardLayout 
      userId={userId} 
      userRole={userRole}
    />
  );
}

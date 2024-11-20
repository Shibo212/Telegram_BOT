import React from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import {
  UsersIcon,
  BookOpenIcon,
  AcademicCapIcon,
  UserGroupIcon,
} from '@heroicons/react/24/outline';

const StatCard = ({ title, value, icon: Icon }: { title: string; value: number; icon: any }) => (
  <div className="bg-white p-6 rounded-lg shadow-md">
    <div className="flex items-center">
      <div className="p-3 rounded-full bg-indigo-100">
        <Icon className="h-6 w-6 text-indigo-600" />
      </div>
      <div className="ml-4">
        <p className="text-sm font-medium text-gray-500">{title}</p>
        <p className="text-2xl font-semibold text-gray-900">{value}</p>
      </div>
    </div>
  </div>
);

export default function Dashboard() {
  const { data: stats, isLoading, isError, error } = useQuery('stats', async () => {
    const { data } = await axios.get('http://localhost:8000/api/stats');
    return data;
  });

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-8">
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">
                Error loading dashboard data. Please try again later.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const defaultStats = {
    total_users: 0,
    total_lessons: 0,
    total_quizzes: 0,
    active_users: 0,
    ...stats
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Users"
          value={defaultStats.total_users}
          icon={UsersIcon}
        />
        <StatCard
          title="Total Lessons"
          value={defaultStats.total_lessons}
          icon={BookOpenIcon}
        />
        <StatCard
          title="Total Quizzes"
          value={defaultStats.total_quizzes}
          icon={AcademicCapIcon}
        />
        <StatCard
          title="Active Users"
          value={defaultStats.active_users}
          icon={UserGroupIcon}
        />
      </div>
    </div>
  );
}
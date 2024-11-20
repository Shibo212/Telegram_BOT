import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  BookOpenIcon,
  AcademicCapIcon,
  UsersIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Lessons', href: '/lessons', icon: BookOpenIcon },
  { name: 'Quizzes', href: '/quizzes', icon: AcademicCapIcon },
  { name: 'Users', href: '/users', icon: UsersIcon },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col h-0 flex-1">
          <div className="flex items-center h-16 flex-shrink-0 px-4 bg-indigo-700">
            <h1 className="text-xl font-bold text-white">Dutch Learning Bot</h1>
          </div>
          <div className="flex-1 flex flex-col overflow-y-auto bg-indigo-800">
            <nav className="flex-1 px-2 py-4 space-y-1">
              {navigation.map((item) => {
                const current = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`${
                      current
                        ? 'bg-indigo-900 text-white'
                        : 'text-indigo-100 hover:bg-indigo-600'
                    } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                  >
                    <item.icon
                      className="mr-3 flex-shrink-0 h-6 w-6"
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
}
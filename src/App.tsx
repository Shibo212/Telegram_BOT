import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import Dashboard from './pages/Dashboard';
import Lessons from './pages/Lessons';
import Sidebar from './components/Sidebar';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000,
      cacheTime: 10 * 60 * 1000,
      onError: (error) => {
        console.error('Query Error:', error);
      }
    },
    mutations: {
      onError: (error) => {
        console.error('Mutation Error:', error);
      }
    }
  }
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="flex h-screen bg-gray-100">
          <Sidebar />
          <div className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/lessons" element={<Lessons />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
      <Toaster position="top-right" />
    </QueryClientProvider>
  );
}
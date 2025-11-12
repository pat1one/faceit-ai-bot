'use client';
import React from 'react';
import Link from 'next/link';
import { useAuth } from '../src/contexts/AuthContext';

export default function HomePage() {
  const { user } = useAuth();
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-8">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-6xl font-bold mb-6"><span className="gradient-text">Faceit AI Bot</span></h1>
        <p className="text-xl text-zinc-600 dark:text-zinc-400 mb-12 max-w-2xl mx-auto">Advanced CS2 statistics analysis and teammate search platform</p>
        <div className="flex gap-4 justify-center mb-16">
          {user ? (
            <Link href="/dashboard" className="px-8 py-4 bg-gradient-to-r from-primary to-primary-dark rounded-lg text-lg font-semibold text-white hover:-translate-y-1 transition-transform">Dashboard</Link>
          ) : (
            <><Link href="/auth" className="px-8 py-4 bg-gradient-to-r from-primary to-primary-dark rounded-lg text-lg font-semibold text-white hover:-translate-y-1 transition-transform">Get Started</Link>
            <Link href="/auth" className="px-8 py-4 glass-effect rounded-lg text-lg font-medium text-white hover:bg-white/10 transition-colors">Sign In</Link></>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          <div className="glass-effect rounded-2xl p-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur"><div className="text-4xl mb-4">📊</div><h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Demo Analysis</h3><p className="text-zinc-600 dark:text-zinc-400">Upload and analyze CS2 demos</p></div>
          <div className="glass-effect rounded-2xl p-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur"><div className="text-4xl mb-4">🎯</div><h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Player Stats</h3><p className="text-zinc-600 dark:text-zinc-400">Track your performance</p></div>
          <div className="glass-effect rounded-2xl p-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur"><div className="text-4xl mb-4">👥</div><h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Find Teammates</h3><p className="text-zinc-600 dark:text-zinc-400">Connect with players</p></div>
        </div>
      </div>
    </div>
  );
}

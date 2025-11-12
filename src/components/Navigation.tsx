'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';
import LanguageSwitcher from './LanguageSwitcher';
import ThemeSwitcher from './ThemeSwitcher';

const Navigation = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="fixed top-0 left-0 right-0 bg-[#0c0c0c]/95 dark:bg-black/95 backdrop-blur-lg border-b border-white/10 dark:border-gray-800/10 z-50">
      <div className="max-w-[1400px] mx-auto px-8 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 text-xl font-bold text-white dark:text-white hover:opacity-80 transition-opacity">
          <span className="text-2xl">🎮</span>
          <span>Faceit AI Bot</span>
        </Link>
        
        <div className="flex gap-8">
          <Link href="/" className="text-zinc-400 dark:text-zinc-300 font-medium hover:text-white dark:hover:text-white transition-colors">
            Home
          </Link>
          <Link href="/demo" className="text-zinc-400 dark:text-zinc-300 font-medium hover:text-white dark:hover:text-white transition-colors">
            Demo Analysis
          </Link>
          <Link href="/teammates" className="text-zinc-400 dark:text-zinc-300 font-medium hover:text-white dark:hover:text-white transition-colors">
            Teammates
          </Link>
          {user && (
            <Link href="/dashboard" className="text-zinc-400 dark:text-zinc-300 font-medium hover:text-white dark:hover:text-white transition-colors">
              Dashboard
            </Link>
          )}
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <ThemeSwitcher />
            <LanguageSwitcher />
          </div>
          {user ? (
            <>
              <span className="text-zinc-400 dark:text-zinc-300 text-sm">{user.username || user.email}</span>
              <button 
                onClick={logout} 
                className="px-6 py-2.5 bg-white/10 dark:bg-white/5 border border-white/20 dark:border-white/10 rounded-lg text-white font-medium hover:bg-white/15 dark:hover:bg-white/10 transition-colors"
              >
                Logout
              </button>
            </>
          ) : (
            <Link 
              href="/auth" 
              className="px-6 py-2.5 bg-gradient-to-r from-primary to-primary-dark rounded-lg text-white font-semibold hover:-translate-y-0.5 transition-transform inline-block"
            >
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
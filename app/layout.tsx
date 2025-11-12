import React from 'react';
import './globals.css';
import Navigation from '../src/components/Navigation';
import { Providers } from './providers';
import type { Metadata, Viewport } from 'next';

export const metadata: Metadata = {
  title: 'Faceit AI Bot - Stats Analysis and Teammate Search',
  description: 'Tool for game stats analysis and teammate search on Faceit platform. Download browser extension or full version on our website.',
  icons: {
    icon: '/icon.svg',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#2E9EF7',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#2E9EF7" />
        <link rel="apple-touch-icon" href="/icon-152x152.png" />
      </head>
      <body>
        <Providers>
          <Navigation />
          <main style={{ paddingTop: '80px' }}>{children}</main>
        </Providers>
        <script dangerouslySetInnerHTML={{
          __html: `
            if ('serviceWorker' in navigator) {
              window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                  .then(reg => console.log('Service Worker registered'))
                  .catch(err => console.log('Service Worker registration failed:', err));
              });
            }
          `
        }} />
      </body>
    </html>
  );
}

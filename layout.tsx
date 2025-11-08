import './globals.css';
import Navigation from '../components/Navigation';
import type { Metadata, Viewport } from 'next';

export const metadata: Metadata = {
  title: 'Faceit AI Bot',
  description: 'AI-ассистент для Faceit и CS2',
  keywords: 'CS2, Counter-Strike, AI, анализ демок, тиммейты, Faceit',
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body>
        <Navigation />
        <main style={{ paddingTop: '80px' }}>
          {children}
        </main>
      </body>
    </html>
  );
}

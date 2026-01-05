'use client';

import React, { useEffect, useState } from 'react';

export default function MetricsPage() {
  const [text, setText] = useState<string>('');
  const [error, setError] = useState<string>('');

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const res = await fetch('/api/metrics', {
          method: 'GET',
          headers: {
            Accept: 'text/plain',
          },
        });

        if (!res.ok) {
          const body = await res.text();
          if (!cancelled) {
            setError(body || `HTTP ${res.status}`);
          }
          return;
        }

        const body = await res.text();
        if (!cancelled) {
          setText(body);
        }
      } catch (e: any) {
        if (!cancelled) {
          setError(e?.message || 'Failed to load metrics');
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="min-h-screen px-6 py-20">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-4 text-white">Metrics</h1>

        {error ? (
          <div className="p-3 bg-red-900/20 border border-red-800 rounded-lg text-red-300 text-sm">
            {error}
          </div>
        ) : (
          <pre className="whitespace-pre-wrap break-words text-xs bg-gray-900/60 border border-gray-800 rounded-lg p-4 text-gray-100 overflow-auto">
            {text || 'Loading...'}
          </pre>
        )}
      </div>
    </div>
  );
}

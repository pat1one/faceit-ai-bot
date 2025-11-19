'use client';

import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useTranslation } from 'react-i18next';
import API_ENDPOINTS from '../../src/config/api';

export default function DemoPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { t, i18n } = useTranslation();
  const coachReport = (result as any)?.coach_report;

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-white flex items-center justify-center animate-fade-in">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-8 text-white">{t('demo.title')}</h1>
          <button 
            onClick={() => router.push('/auth')} 
            className="btn-primary"
          >
            {t('landing.cta_sign_in')}
          </button>
        </div>
      </div>
    );
  }

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('demo', file);

      const lang = i18n.language && i18n.language.toLowerCase().startsWith('en')
        ? 'en'
        : 'ru';

      const response = await fetch(`${API_ENDPOINTS.DEMO_ANALYZE}?language=${lang}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const text = await response.text();
        setError(text || t('demo.error_sbp'));
        return;
      }

      const data = await response.json();
      setResult(data);
    } catch (e) {
      console.error('Demo analyze error', e);
      setError(t('demo.error_sbp'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-white animate-fade-in">
      <div className="text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent">📊 {t('demo.title')}</h1>
          <p className="text-xl text-gray-300 mb-8">{t('demo.subtitle')}</p>
        
        <div className="glass-effect rounded-2xl p-8 animate-fade-in-up">
          <div className="border-2 border-dashed border-zinc-600 rounded-xl p-12 text-center">
            <input
              type="file"
              accept=".dem"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="hidden"
              id="demo-upload"
            />
            <label htmlFor="demo-upload" className="cursor-pointer">
              <div className="text-6xl mb-4">📁</div>
              <p className="text-xl mb-2">{file ? file.name : t('demo.upload_label')}</p>
              <p className="text-sm text-zinc-500">.dem</p>
            </label>
          </div>
          
          {file && (
            <button
              onClick={handleUpload}
              disabled={loading}
              className="w-full mt-6 btn-primary disabled:opacity-50"
            >
              {loading ? t('demo.analyzing') : t('demo.upload_button')}
            </button>
          )}
        </div>
        {error && (
          <p className="mt-4 text-red-400 text-sm">{error}</p>
        )}
        {loading && (
          <div className="mt-8 text-left text-sm card animate-pulse">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4" />
            <div className="space-y-2">
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full" />
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-11/12" />
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-10/12" />
            </div>
          </div>
        )}
        {result && (
          <div className="mt-8 text-left max-h-96 overflow-auto text-sm card">
            <h2 className="text-lg font-semibold mb-2">{t('demo.results')}</h2>
            {coachReport ? (
              <div className="space-y-4">
                {coachReport.overview && (
                  <p className="text-sm text-zinc-300 mb-2">
                    {coachReport.overview}
                  </p>
                )}

                {coachReport.strengths && coachReport.strengths.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-1">
                      {t('demo.coach_strengths', { defaultValue: 'Сильные стороны' })}
                    </h3>
                    <ul className="list-disc list-inside space-y-1 text-sm">
                      {coachReport.strengths.map((s: any, idx: number) => (
                        <li key={idx}>
                          <span className="font-medium">{s.title}: </span>
                          <span>{s.description}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {coachReport.weaknesses && coachReport.weaknesses.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-1">
                      {t('demo.coach_weaknesses', { defaultValue: 'Слабые стороны' })}
                    </h3>
                    <ul className="list-disc list-inside space-y-1 text-sm">
                      {coachReport.weaknesses.map((w: any, idx: number) => (
                        <li key={idx}>
                          <span className="font-medium">{w.title}: </span>
                          <span>{w.description}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {coachReport.key_moments && coachReport.key_moments.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-1">
                      {t('demo.coach_key_moments', { defaultValue: 'Ключевые моменты' })}
                    </h3>
                    <ul className="space-y-1 text-sm">
                      {coachReport.key_moments.map((m: any, idx: number) => (
                        <li key={idx} className="border border-zinc-700 rounded-md p-2">
                          <div className="text-xs text-zinc-400 mb-1">
                            {t('demo.round_label', { defaultValue: 'Раунд' })} {m.round}
                          </div>
                          <div className="font-medium mb-1">{m.title}</div>
                          <div className="text-xs text-zinc-300 mb-1">{m.what_happened}</div>
                          <div className="text-xs text-red-300 mb-1">{m.mistake}</div>
                          <div className="text-xs text-emerald-300">{m.better_play}</div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {coachReport.training_plan && coachReport.training_plan.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-1">
                      {t('demo.coach_training_plan', { defaultValue: 'План тренировок' })}
                    </h3>
                    <ul className="space-y-2 text-sm">
                      {coachReport.training_plan.map((p: any, idx: number) => (
                        <li key={idx} className="border border-zinc-700 rounded-md p-2">
                          <div className="font-medium mb-1">{p.goal}</div>
                          {p.exercises && (
                            <ul className="list-disc list-inside text-xs text-zinc-300 space-y-1">
                              {p.exercises.map((ex: string, exIdx: number) => (
                                <li key={exIdx}>{ex}</li>
                              ))}
                            </ul>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {coachReport.summary && (
                  <p className="text-sm text-zinc-200">
                    {coachReport.summary}
                  </p>
                )}
              </div>
            ) : (
              <pre className="whitespace-pre-wrap break-all">{JSON.stringify(result, null, 2)}</pre>
            )}
          </div>
        )}
        </div>
      </div>
    </div>
  );
}

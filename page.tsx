'use client';

import React from 'react';
import DemoUpload from '../../components/DemoUpload';

export default function DemoPage() {
  const handleAnalysisComplete = (result: any) => {
    console.log('Demo analysis completed:', result);
  };

  return (
    <div className="page-container">
      <div className="container">
        <div className="page-header">
          <h1>AI-Анализ демок</h1>
          <p>Загрузите свою демку CS2 для получения подробного анализа игры и персональных рекомендаций</p>
        </div>

        <DemoUpload onAnalysisComplete={handleAnalysisComplete} />

        <div className="features-info">
          <h3>Что вы получите:</h3>
          <div className="feature-list">
            <div className="feature-item">
              <span className="feature-emoji">🎯</span>
              <div>
                <strong>Анализ точности</strong>
                <p>Подробная статистика стрельбы и рекомендации по улучшению</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-emoji">📊</span>
              <div>
                <strong>Производительность по картам</strong>
                <p>Анализ игры на разных картах и слабых зон</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-emoji">🧠</span>
              <div>
                <strong>Тактические советы</strong>
                <p>AI-рекомендации по позиционированию и игровой логике</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-emoji">⚔️</span>
              <div>
                <strong>Анализ оружия</strong>
                <p>Статистика использования оружия и эффективность</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .page-container {
          min-height: 100vh;
          padding: 2rem 0;
          background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
        }

        .page-header {
          text-align: center;
          margin-bottom: 3rem;
        }

        .page-header h1 {
          font-size: 3rem;
          font-weight: 800;
          margin-bottom: 1rem;
          background: linear-gradient(45deg, #ff5200, #ffaa00);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .page-header p {
          font-size: 1.2rem;
          color: #a1a1aa;
          max-width: 600px;
          margin: 0 auto;
          line-height: 1.6;
        }

        .features-info {
          margin-top: 4rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 16px;
          padding: 2rem;
          backdrop-filter: blur(10px);
        }

        .features-info h3 {
          margin-bottom: 2rem;
          color: #fafafa;
          text-align: center;
        }

        .feature-list {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1.5rem;
        }

        .feature-item {
          display: flex;
          gap: 1rem;
          align-items: flex-start;
        }

        .feature-emoji {
          font-size: 2rem;
          flex-shrink: 0;
        }

        .feature-item strong {
          color: #fafafa;
          display: block;
          margin-bottom: 0.5rem;
        }

        .feature-item p {
          color: #a1a1aa;
          font-size: 0.9rem;
          line-height: 1.4;
        }
      `}</style>
    </div>
  );
}
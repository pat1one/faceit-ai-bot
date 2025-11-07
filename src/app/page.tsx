'use client';

import React, { useState } from 'react';

type AnalysisResult = {
  accuracy: number;
  recommendations: string[];
};
import DemoUpload from '../components/DemoUpload';
import TeammateChat from '../components/TeammateChat';
import NotificationSystem from '../components/NotificationSystem';

export default function DemoPage() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [paymentUrl, setPaymentUrl] = useState(null);

  const handleAnalysisComplete = async (file) => {
    setLoading(true);
    setAnalysisResult(null);

    try {
      const formData = new FormData();
      formData.append('demo', file);

      const response = await fetch('http://localhost:8000/analyze-demo', {
        method: 'POST',
        body: formData,
      });

      await new Promise(resolve => setTimeout(resolve, 100)); // Небольшая задержка чтобы загрузка была видна
      
      const result = await response.json();
      console.log('Analysis response:', result);
      
      if (result.status === 'success') {
        console.log('Setting analysis result:', result.data);
        setAnalysisResult(result.data);
      } else {
        console.error('Analysis failed:', result);
        throw new Error('Analysis failed');
      }
    } catch (error) {
      console.error('Error during analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async () => {
    try {
      const response = await fetch('http://localhost:8000/payments/yookassa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: 500,
          currency: 'RUB',
          description: 'Оплата анализа демки',
        }),
      });

      const paymentData = await response.json();
      setPaymentUrl(paymentData.payment_url);
    } catch (error) {
      console.error('Error during payment:', error);
    }
  };

  const handleSBPPayment = async () => {
    try {
      const response = await fetch('http://localhost:8000/payments/sbp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: 500,
          currency: 'RUB',
          description: 'Оплата анализа демки через СБП',
        }),
      });

      const paymentData = await response.json();
      setPaymentUrl(paymentData.payment_url);
    } catch (error) {
      console.error('Error during SBP payment:', error);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>AI-Анализ демок</h1>
        <p>Загрузите свою демку CS2 для получения подробного анализа игры и персональных рекомендаций</p>
      </div>

      <DemoUpload onAnalysisComplete={handleAnalysisComplete} />

      {loading ? (
        <div className="loading-container" data-testid="loading-indicator">
          <div className="loading-spinner"></div>
          <div className="loading-text">Анализируем демку...</div>
        </div>
      ) : null}

      {analysisResult && (
        <div className="analysis-result">
          <h3>Результаты анализа</h3>
          <p>Точность: {analysisResult.accuracy * 100}%</p>
          <h4>Рекомендации:</h4>
          <ul>
            {analysisResult.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
          <div className="payment-buttons">
            <button onClick={handlePayment} className="btn btn-primary">Оплатить через YooKassa</button>
            <button onClick={handleSBPPayment} className="btn btn-secondary">Оплатить через СБП</button>
          </div>
        </div>
      )}

      {paymentUrl && (
        <div className="payment-link">
          <p>Перейдите по ссылке для оплаты:</p>
          <a href={paymentUrl} target="_blank" rel="noopener noreferrer">Оплатить</a>
        </div>
      )}

      <TeammateChat />
      <NotificationSystem />

      <style>{`
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

        .analysis-result {
          margin-top: 2rem;
          padding: 1rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 8px;
          color: #fafafa;
        }

        .analysis-result pre {
          white-space: pre-wrap;
          word-wrap: break-word;
        }

        .btn {
          margin-top: 1rem;
          padding: 0.5rem 1rem;
          background: #ff5200;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .btn:hover {
          background: #ffaa00;
        }

        .btn-secondary {
          margin-top: 1rem;
          padding: 0.5rem 1rem;
          background: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .btn-secondary:hover {
          background: #0056b3;
        }

        .payment-link {
          margin-top: 2rem;
          padding: 1rem;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 8px;
          color: #fafafa;
        }

        .payment-link a {
          color: #ffaa00;
          text-decoration: none;
        }

        .payment-link a:hover {
          text-decoration: underline;
        }

        .feature-item p {
          color: #a1a1aa;
          font-size: 0.9rem;
          line-height: 1.4;
        }

        .loading-container {
          text-align: center;
          margin: 20px 0;
        }

        .loading-text {
          color: #ff9900;
          font-size: 1.2rem;
          margin-top: 10px;
        }

        .loading-spinner {
          width: 40px;
          height: 40px;
          margin: 0 auto;
          border: 4px solid #f3f3f3;
          border-top: 4px solid #ff9900;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }      `}</style>    </div>  );}
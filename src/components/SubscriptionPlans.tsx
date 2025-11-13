'use client';

import React, { useState } from 'react';

const SubscriptionPlans = () => {
  const [loading, setLoading] = useState(false);
  
  const plans = [
    { 
      level: 'FREE', 
      price: 0, 
      features: ['5 анализов в месяц', 'Базовая статистика', 'Поиск тиммейтов'],
      popular: false
    },
    { 
      level: 'BASIC', 
      price: 299, 
      features: ['50 анализов в месяц', 'Детальная статистика', 'Анализ демок', 'AI рекомендации'],
      popular: false
    },
    { 
      level: 'PRO', 
      price: 599, 
      features: ['Безлимитные анализы', 'Продвинутая аналитика', 'Приоритетная поддержка', 'Экспорт данных'],
      popular: true
    },
    { 
      level: 'ELITE', 
      price: 999, 
      features: ['Все функции PRO', 'Персональный тренер', 'API доступ', 'Белый лейбл'],
      popular: false
    },
  ];

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Subscriptions</h1>
      <div style={{ display: 'flex', gap: '20px' }}>
        {plans.map((plan) => (
          <div
            key={plan.level}
            style={{
              border: '1px solid #ccc',
              borderRadius: '10px',
              padding: '20px',
              width: '200px',
              textAlign: 'center',
            }}
          >
            <h2>{plan.level}</h2>
            <p>Price: ${plan.price}/month</p>
            <ul>
              {plan.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
            <button
              style={{
                padding: '10px 20px',
                backgroundColor: '#007BFF',
                color: '#fff',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
              }}
            >
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SubscriptionPlans;
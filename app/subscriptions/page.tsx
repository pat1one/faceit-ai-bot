'use client';

import React from 'react';
import { useAuth } from '../../src/contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function SubscriptionsPage() {
  const { user } = useAuth();
  const router = useRouter();

  const plans = [
    { tier: 'FREE', price: 0, features: ['5 анализов', 'Базовая статистика'] },
    { tier: 'BASIC', price: 299, features: ['50 анализов', 'Детальная статистика'], popular: false },
    { tier: 'PRO', price: 599, features: ['Безлимит', 'AI анализ'], popular: true },
    { tier: 'ELITE', price: 999, features: ['Все функции', 'API доступ'] }
  ];

  const handleSelect = (tier: string, price: number) => {
    if (!user) {
      router.push('/auth');
      return;
    }
    
    if (price === 0) {
      alert('Бесплатный план активирован!');
    } else {
      alert(`Оплата ${tier}: ${price}₽/месяц`);
    }
  };

  return (
    <div className="min-h-screen py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold hero-gradient mb-6">Подписки</h1>
          <p className="text-xl text-gray-300">Выберите план для CS2 анализа</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {plans.map((plan) => (
            <div key={plan.tier} className={`card ${plan.popular ? 'ring-2 ring-orange-500' : ''}`}>
              {plan.popular && (
                <div className="text-center mb-4">
                  <span className="bg-orange-500 text-white px-3 py-1 rounded-full text-sm">
                    Популярный
                  </span>
                </div>
              )}
              
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">{plan.tier}</h3>
                <div className="text-3xl font-bold text-white mb-4">
                  {plan.price === 0 ? 'Бесплатно' : `₽${plan.price}/мес`}
                </div>
              </div>

              <ul className="space-y-2 mb-6">
                {plan.features.map((feature, i) => (
                  <li key={i} className="text-gray-300 flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleSelect(plan.tier, plan.price)}
                className="w-full btn-primary"
              >
                Выбрать
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

import React from 'react';

const SubscriptionPlans = () => {
  const plans = [
    { level: 'Basic', price: 10, features: ['Feature 1', 'Feature 2'] },
    { level: 'Pro', price: 20, features: ['Feature 1', 'Feature 2', 'Feature 3'] },
    { level: 'Premium', price: 30, features: ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4'] },
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
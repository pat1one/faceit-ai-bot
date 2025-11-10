import React from 'react';

const AccountPage = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Account</h1>
      <p>Welcome to your account. Here you can manage your profile and settings.</p>
      <button style={{ padding: '10px 20px', backgroundColor: '#007BFF', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        Edit Profile
      </button>
    </div>
  );
};

export default AccountPage;
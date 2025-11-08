import React from 'react';

const AccountPage = () => {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Личный кабинет</h1>
      <p>Добро пожаловать в ваш личный кабинет. Здесь вы можете управлять своим профилем и настройками.</p>
      <button style={{ padding: '10px 20px', backgroundColor: '#007BFF', color: '#fff', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        Редактировать профиль
      </button>
    </div>
  );
};

export default AccountPage;
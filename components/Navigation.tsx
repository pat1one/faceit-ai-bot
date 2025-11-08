import React from 'react';

export default function Navigation() {
  return (
    <nav style={{
      height: 64,
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      background: '#0b0b0b',
      color: '#fff',
      display: 'flex',
      alignItems: 'center',
      padding: '0 1rem',
      zIndex: 1000,
    }}>
      <div style={{fontWeight: 700}}>Faceit AI Bot</div>
    </nav>
  );
}

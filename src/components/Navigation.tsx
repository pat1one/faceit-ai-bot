import React from 'react';
import { toggleDarkMode } from '../utils/darkModeToggle';

const Navigation = () => {
  return (
    <nav style={{ padding: '10px', backgroundColor: '#007BFF', color: '#fff', display: 'flex', justifyContent: 'space-between' }}>
      <h1>Faceit AI Bot</h1>
      <button
        onClick={toggleDarkMode}
        style={{
          padding: '10px 20px',
          backgroundColor: '#fff',
          color: '#007BFF',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Toggle Dark Mode
      </button>
    </nav>
  );
};

export default Navigation;
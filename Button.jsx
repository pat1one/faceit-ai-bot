import React from "react";

export function Button({ children, ...props }) {
  return (
    <button style={{
      background: '#2563eb', color: '#fff', border: 'none', borderRadius: 6, padding: '8px 20px', fontSize: 16, cursor: 'pointer'
    }} {...props}>
      {children}
    </button>
  );
}

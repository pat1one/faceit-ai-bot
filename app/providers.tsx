'use client';

import React, { useEffect } from 'react';
import '../src/i18n/config';

export function Providers({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize i18n on client side
  }, []);

  return <>{children}</>;
}

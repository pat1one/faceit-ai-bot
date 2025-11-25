'use client';

import React, { useEffect, useRef } from 'react';

interface Props {
  onTokenChange: (token: string | null) => void;
}

const siteKey = process.env.NEXT_PUBLIC_SMARTCAPTCHA_SITE_KEY;

export default function SmartCaptchaWidget({ onTokenChange }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const callbackNameRef = useRef<string>(
    `smartCaptchaCallback_${Math.random().toString(36).slice(2)}`,
  );

  useEffect(() => {
    if (!siteKey) {
      return;
    }

    let cancelled = false;

    const loadScript = () => {
      return new Promise<void>((resolve, reject) => {
        if (typeof window === 'undefined') {
          resolve();
          return;
        }

        const existing = document.querySelector(
          'script[data-smartcaptcha-script="true"]',
        ) as HTMLScriptElement | null;

        if (existing) {
          resolve();
          return;
        }

        const script = document.createElement('script');
        script.src = 'https://smartcaptcha.yandexcloud.net/smartcaptcha.js';
        script.async = true;
        script.defer = true;
        script.setAttribute('data-smartcaptcha-script', 'true');
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load SmartCaptcha script'));
        document.head.appendChild(script);
      });
    };

    if (typeof window !== 'undefined') {
      (window as any)[callbackNameRef.current] = (token: string) => {
        onTokenChange(token || null);
      };
    }

    loadScript()
      .then(() => {
        if (cancelled) return;
        if (!containerRef.current) return;
      })
      .catch(() => {
        onTokenChange(null);
      });

    return () => {
      cancelled = true;
      onTokenChange(null);
      if (typeof window !== 'undefined') {
        try {
          delete (window as any)[callbackNameRef.current];
        } catch {
          // ignore
        }
      }
    };
  }, [onTokenChange]);

  if (!siteKey) {
    return null;
  }

  return (
    <div className="flex justify-center mt-4">
      <div
        ref={containerRef}
        className="smart-captcha"
        data-sitekey={siteKey}
        data-callback={callbackNameRef.current}
      />
    </div>
  );
}

/**
 * Analytics component for tracking
 */

import Script from 'next/script';

export function Analytics() {
  const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID;
  const PLAUSIBLE_DOMAIN = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN;

  return (
    <>
      {/* Google Analytics */}
      {GA_TRACKING_ID && (
        <>
          <Script
            src={`https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`}
            strategy="afterInteractive"
          />
          <Script id="google-analytics" strategy="afterInteractive">
            {`
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${GA_TRACKING_ID}', {
                anonymize_ip: true,
                cookie_flags: 'SameSite=None;Secure'
              });
            `}
          </Script>
        </>
      )}

      {/* Plausible Analytics (Privacy-friendly) */}
      {PLAUSIBLE_DOMAIN && (
        <Script
          defer
          data-domain={PLAUSIBLE_DOMAIN}
          src="https://plausible.io/js/script.js"
        />
      )}
    </>
  );
}

// Event tracking helpers
export const analytics = {
  pageview: (url: string) => {
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('config', process.env.NEXT_PUBLIC_GA_ID, {
        page_path: url,
      });
    }
  },

  event: ({ action, category, label, value }: {
    action: string;
    category: string;
    label?: string;
    value?: number;
  }) => {
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('event', action, {
        event_category: category,
        event_label: label,
        value: value,
      });
    }
  },
};

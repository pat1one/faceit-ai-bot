import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

const SITE_BASE = 'https://pattmsc.online';
const API_BASE = SITE_BASE + '/api';
const TOKEN_KEY = 'faceit_ai_bot_access_token';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface UserInfo {
  id: number;
  email?: string;
  username?: string;
}

function openInNewTab(path: string) {
  const url = SITE_BASE + path;
  if ((window as any).chrome?.tabs?.create) {
    (window as any).chrome.tabs.create({ url });
  } else {
    window.open(url, '_blank');
  }
}

const Popup: React.FC = () => {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState<boolean>(false);

  useEffect(() => {
    const controller = new AbortController();

    const loadFromToken = async () => {
      const storedToken = window.localStorage.getItem(TOKEN_KEY);
      if (!storedToken) {
        setLoading(false);
        return;
      }

      setToken(storedToken);

      try {
        const res = await fetch(API_BASE + '/auth/me', {
          headers: {
            Authorization: `Bearer ${storedToken}`,
          },
          signal: controller.signal,
        });

        if (!res.ok) {
          setUser(null);
        } else {
          const data = await res.json();
          setUser(data);
        }
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadFromToken();
    return () => controller.abort();
  }, []);

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setAuthLoading(true);
    setAuthError(null);

    try {
      const res = await fetch(API_BASE + '/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!res.ok) {
        setAuthError('Login failed. Check your credentials.');
        return;
      }

      const data = (await res.json()) as LoginResponse;
      if (!data.access_token) {
        setAuthError('No access token returned from API.');
        return;
      }

      window.localStorage.setItem(TOKEN_KEY, data.access_token);
      setToken(data.access_token);

      const meRes = await fetch(API_BASE + '/auth/me', {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });

      if (meRes.ok) {
        const meData = await meRes.json();
        setUser(meData);
      } else {
        setUser(null);
      }
    } catch {
      setAuthError('Network error. Please try again.');
    } finally {
      setAuthLoading(false);
      setLoading(false);
    }
  };

  const handleLogout = () => {
    window.localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  };

  const name = user?.username || user?.email || 'Player';

  return (
    <div className="popup-root">
      <header className="popup-header">
        <div className="popup-title">Faceit AI Bot</div>
        <div className="popup-subtitle">
          AI demo coach and teammate search for CS2
        </div>
      </header>

      <main className="popup-main">
        {loading ? (
          <div style={{ fontSize: 12, color: '#9ca3af' }}>Checking extension session...</div>
        ) : user ? (
          <>
            <div style={{ fontSize: 12, color: '#9ca3af' }}>Signed in as {name}</div>
            <button
              className="btn-primary"
              onClick={() => openInNewTab('/analysis?auto=1')}
            >
              Analyze my account
            </button>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/demo')}
            >
              Demo analysis
            </button>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/teammates')}
            >
              Teammates
            </button>
            <button
              className="btn-secondary"
              onClick={handleLogout}
            >
              Sign out in extension
            </button>
          </>
        ) : (
          <>
            <div style={{ fontSize: 12, color: '#9ca3af' }}>
              Log in with your Faceit AI Bot account to use the extension.
            </div>
            <form
              onSubmit={handleLogin}
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 6,
                marginTop: 6,
              }}
            >
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{
                  padding: '6px 8px',
                  borderRadius: 6,
                  border: '1px solid #374151',
                  backgroundColor: '#020617',
                  color: '#f9fafb',
                  fontSize: 12,
                }}
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  padding: '6px 8px',
                  borderRadius: 6,
                  border: '1px solid #374151',
                  backgroundColor: '#020617',
                  color: '#f9fafb',
                  fontSize: 12,
                }}
              />
              {authError && (
                <div style={{ fontSize: 11, color: '#f87171' }}>{authError}</div>
              )}
              <button
                type="submit"
                className="btn-primary"
                disabled={authLoading}
              >
                {authLoading ? 'Logging in...' : 'Log in'}
              </button>
            </form>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/auth')}
            >
              Open auth page
            </button>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/demo/example')}
            >
              Demo analysis example
            </button>
          </>
        )}
      </main>

      <footer className="popup-footer">
        <span className="popup-hint">
          The extension uses an API token stored in the extension (not browser cookies).
        </span>
      </footer>
    </div>
  );
}

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<Popup />);
}

import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

const SITE_BASE = 'https://pattmsc.online';
const API_BASE = SITE_BASE + '/api';

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
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const controller = new AbortController();
    const loadMe = async () => {
      try {
        const res = await fetch(API_BASE + '/auth/me', {
          credentials: 'include',
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

    loadMe();
    return () => controller.abort();
  }, []);

  const name = user?.username || user?.email || 'Игрок';

  return (
    <div className="popup-root">
      <header className="popup-header">
        <div className="popup-title">Faceit AI Bot</div>
        <div className="popup-subtitle">
          Быстрый доступ к анализу игрока, демок и тиммейтов
        </div>
      </header>

      <main className="popup-main">
        {loading ? (
          <div style={{ fontSize: 12, color: '#9ca3af' }}>Проверяем сессию...</div>
        ) : user ? (
          <>
            <div style={{ fontSize: 12, color: '#9ca3af' }}>Вошёл как {name}</div>
            <button
              className="btn-primary"
              onClick={() => openInNewTab('/analysis?auto=1')}
            >
              Анализ моего аккаунта
            </button>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/demo')}
            >
              Анализ демки
            </button>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/teammates')}
            >
              Тиммейты
            </button>
          </>
        ) : (
          <>
            <div style={{ fontSize: 12, color: '#9ca3af' }}>
              Не выполнен вход. Залогинься, чтобы получать персональный разбор.
            </div>
            <button
              className="btn-primary"
              onClick={() => openInNewTab('/auth')}
            >
              Войти / Зарегистрироваться
            </button>
            <button
              className="btn-secondary"
              onClick={() => openInNewTab('/demo/example')}
            >
              Пример анализа демки
            </button>
          </>
        )}
      </main>

      <footer className="popup-footer">
        <span className="popup-hint">
          Расширение использует ту же httpOnly-сессию, что и сайт.
        </span>
      </footer>
    </div>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<Popup />);
}

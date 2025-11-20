const SITE_BASE = "https://pattmsc.online";
const API_BASE = SITE_BASE + "/api";

function openInNewTab(path) {
  const url = SITE_BASE + path;
  if (typeof chrome !== "undefined" && chrome.tabs && chrome.tabs.create) {
    chrome.tabs.create({ url });
  } else {
    window.open(url, "_blank");
  }
}

function createButton(text, className, onClick) {
  const btn = document.createElement("button");
  btn.textContent = text;
  btn.className = className;
  btn.addEventListener("click", onClick);
  return btn;
}

function renderPopupLoading(root) {
  root.innerHTML = "";
  const container = document.createElement("div");
  container.className = "popup-root";

  const header = document.createElement("header");
  header.className = "popup-header";
  const title = document.createElement("div");
  title.className = "popup-title";
  title.textContent = "Faceit AI Bot";
  const subtitle = document.createElement("div");
  subtitle.className = "popup-subtitle";
  subtitle.textContent = "Проверяем сессию...";
  header.appendChild(title);
  header.appendChild(subtitle);

  const main = document.createElement("main");
  main.className = "popup-main";

  container.appendChild(header);
  container.appendChild(main);

  const footer = document.createElement("footer");
  footer.className = "popup-footer";
  const hint = document.createElement("span");
  hint.className = "popup-hint";
  hint.textContent = "Расширение использует ту же httpOnly-сессию, что и сайт.";
  footer.appendChild(hint);

  container.appendChild(footer);
  root.appendChild(container);
}

function renderPopupLoggedIn(root, user) {
  root.innerHTML = "";
  const container = document.createElement("div");
  container.className = "popup-root";

  const header = document.createElement("header");
  header.className = "popup-header";
  const title = document.createElement("div");
  title.className = "popup-title";
  title.textContent = "Faceit AI Bot";
  const subtitle = document.createElement("div");
  subtitle.className = "popup-subtitle";
  const name = user.username || user.email || "Игрок";
  subtitle.textContent = "Вошёл как " + name;
  header.appendChild(title);
  header.appendChild(subtitle);

  const main = document.createElement("main");
  main.className = "popup-main";

  const btnPlayer = createButton(
    "Анализ моего аккаунта",
    "btn-primary",
    () => openInNewTab("/analysis?auto=1")
  );
  const btnDemo = createButton(
    "Анализ демки",
    "btn-secondary",
    () => openInNewTab("/demo")
  );
  const btnTeam = createButton(
    "Тиммейты",
    "btn-secondary",
    () => openInNewTab("/teammates")
  );

  main.appendChild(btnPlayer);
  main.appendChild(btnDemo);
  main.appendChild(btnTeam);

  const footer = document.createElement("footer");
  footer.className = "popup-footer";
  const hint = document.createElement("span");
  hint.className = "popup-hint";
  hint.textContent = "Расширение использует ту же httpOnly-сессию, что и сайт.";
  footer.appendChild(hint);

  container.appendChild(header);
  container.appendChild(main);
  container.appendChild(footer);
  root.appendChild(container);
}

function renderPopupLoggedOut(root) {
  root.innerHTML = "";
  const container = document.createElement("div");
  container.className = "popup-root";

  const header = document.createElement("header");
  header.className = "popup-header";
  const title = document.createElement("div");
  title.className = "popup-title";
  title.textContent = "Faceit AI Bot";
  const subtitle = document.createElement("div");
  subtitle.className = "popup-subtitle";
  subtitle.textContent =
    "Не выполнен вход. Залогинься, чтобы получать персональный разбор.";
  header.appendChild(title);
  header.appendChild(subtitle);

  const main = document.createElement("main");
  main.className = "popup-main";

  const btnLogin = createButton(
    "Войти / Зарегистрироваться",
    "btn-primary",
    () => openInNewTab("/auth")
  );
  const btnExample = createButton(
    "Пример анализа демки",
    "btn-secondary",
    () => openInNewTab("/demo/example")
  );

  main.appendChild(btnLogin);
  main.appendChild(btnExample);

  const footer = document.createElement("footer");
  footer.className = "popup-footer";
  const hint = document.createElement("span");
  hint.className = "popup-hint";
  hint.textContent = "Расширение использует ту же httpOnly-сессию, что и сайт.";
  footer.appendChild(hint);

  container.appendChild(header);
  container.appendChild(main);
  container.appendChild(footer);
  root.appendChild(container);
}

window.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("root");
  if (!root) return;

  renderPopupLoading(root);

  fetch(API_BASE + "/auth/me", {
    credentials: "include",
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("unauthorized");
      }
      return res.json();
    })
    .then((user) => {
      renderPopupLoggedIn(root, user || {});
    })
    .catch(() => {
      renderPopupLoggedOut(root);
    });
});

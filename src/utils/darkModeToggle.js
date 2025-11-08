// Реализация переключателя тёмного режима
export function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');

  // Сохранение состояния в localStorage
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
}

// Установка темы при загрузке страницы
export function initializeDarkMode() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
  }
}
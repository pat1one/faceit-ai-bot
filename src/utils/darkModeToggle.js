// Dark mode toggle implementation
export function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');

  // Save state to localStorage
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
}

// Initialize theme on page load
export function initializeDarkMode() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
  }
}
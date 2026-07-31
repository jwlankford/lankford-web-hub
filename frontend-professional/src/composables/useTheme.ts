import { ref, onMounted } from 'vue';

export type Theme = 'dark' | 'light';

const theme = ref<Theme>('light');

/**
 * Applies theme to DOM root element.
 */
function applyThemeDOM(t: Theme) {
  theme.value = t;
  if (typeof document !== 'undefined') {
    const root = document.documentElement;
    if (t === 'dark') {
      root.classList.add('dark');
      root.classList.remove('light');
      root.setAttribute('data-theme', 'dark');
    } else {
      root.classList.remove('dark');
      root.classList.add('light');
      root.setAttribute('data-theme', 'light');
    }
  }
}

/**
 * Sets theme explicitly (e.g. on user click) and stores preference in localStorage cache.
 */
export function applyTheme(t: Theme) {
  applyThemeDOM(t);
  if (typeof window !== 'undefined') {
    localStorage.setItem('lankford_hub_theme', t);
  }
}

/**
 * Initializes theme state from localStorage cache, defaulting to 'light' mode always.
 */
export function initTheme() {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('lankford_hub_theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      applyThemeDOM(saved);
    } else {
      applyThemeDOM('light');
    }
  }
}

// Immediately initialize theme on module evaluation
initTheme();

export function useTheme() {
  const toggleTheme = () => {
    const nextTheme: Theme = theme.value === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  };

  onMounted(() => {
    initTheme();
  });

  return {
    theme,
    toggleTheme,
    applyTheme,
  };
}



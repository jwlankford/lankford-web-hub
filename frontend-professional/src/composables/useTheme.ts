import { ref, onMounted } from 'vue';

export type Theme = 'dark' | 'light';

const theme = ref<Theme>('light');

/**
 * Checks Windows / OS system dark mode setting via media query.
 * Returns 'dark' if Windows App Mode is set to Dark, otherwise 'light'.
 */
export function getWindowsSystemTheme(): Theme {
  if (typeof window !== 'undefined' && window.matchMedia) {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    if (window.matchMedia('(prefers-color-scheme: light)').matches) {
      return 'light';
    }
  }
  return 'light';
}

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
 * Sets theme explicitly (on physical user click) and persists to localStorage cache.
 */
export function applyTheme(t: Theme) {
  applyThemeDOM(t);
  if (typeof window !== 'undefined') {
    localStorage.setItem('lankford_hub_theme', t);
  }
}

/**
 * Clears cached localStorage override and resets theme to current Windows OS setting.
 */
export function resetToSystemTheme() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('lankford_hub_theme');
    const systemTheme = getWindowsSystemTheme();
    applyThemeDOM(systemTheme);
  }
}

let mediaQueryListenerAttached = false;

/**
 * Listens for live Windows OS dark/light mode setting changes.
 */
function setupSystemThemeListener() {
  if (typeof window === 'undefined' || !window.matchMedia || mediaQueryListenerAttached) return;

  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  const handleSystemThemeChange = (e: MediaQueryListEvent) => {
    const saved = localStorage.getItem('lankford_hub_theme');
    if (!saved) {
      applyThemeDOM(e.matches ? 'dark' : 'light');
    }
  };

  if (mediaQuery.addEventListener) {
    mediaQuery.addEventListener('change', handleSystemThemeChange);
  } else if ('addListener' in (mediaQuery as any)) {
    (mediaQuery as any).addListener(handleSystemThemeChange);
  }

  mediaQueryListenerAttached = true;
}

/**
 * Initializes theme state from cached user preference or Windows OS dark/light setting.
 */
export function initTheme() {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('lankford_hub_theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      applyThemeDOM(saved);
    } else {
      // Pull Windows OS preference (if Windows is Dark, set Dark; otherwise Light)
      const windowsTheme = getWindowsSystemTheme();
      applyThemeDOM(windowsTheme);
    }
    setupSystemThemeListener();
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
    resetToSystemTheme,
    getWindowsSystemTheme,
  };
}





import { ref, onMounted } from 'vue';

export type Theme = 'dark' | 'light';

const theme = ref<Theme>('dark');
const isSystemPreference = ref<boolean>(true);

/**
 * Returns current OS system theme preference ('dark' or 'light')
 * based on Windows / macOS settings.
 */
export function getSystemTheme(): Theme {
  if (typeof window !== 'undefined' && window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  return 'dark';
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
 * Manually sets theme and persists user override to localStorage.
 */
export function applyTheme(t: Theme) {
  isSystemPreference.value = false;
  applyThemeDOM(t);
  if (typeof window !== 'undefined') {
    localStorage.setItem('lankford_hub_theme', t);
  }
}

/**
 * Resets manual override so theme follows Windows/macOS system settings.
 */
export function resetToSystemTheme() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('lankford_hub_theme');
  }
  isSystemPreference.value = true;
  applyThemeDOM(getSystemTheme());
}

let mediaQueryListenerAttached = false;

/**
 * Listens for live changes in Windows / macOS dark mode system settings.
 */
function setupSystemThemeListener() {
  if (typeof window === 'undefined' || !window.matchMedia || mediaQueryListenerAttached) return;

  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  const handleSystemThemeChange = (e: MediaQueryListEvent) => {
    const saved = localStorage.getItem('lankford_hub_theme');
    if (!saved) {
      isSystemPreference.value = true;
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
 * Initializes theme state from localStorage or OS settings.
 */
export function initTheme() {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('lankford_hub_theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      isSystemPreference.value = false;
      applyThemeDOM(saved);
    } else {
      isSystemPreference.value = true;
      applyThemeDOM(getSystemTheme());
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
    isSystemPreference,
    getSystemTheme,
    toggleTheme,
    applyTheme,
    resetToSystemTheme,
  };
}


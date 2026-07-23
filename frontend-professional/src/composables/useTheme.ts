import { ref, onMounted } from 'vue';

export type Theme = 'dark' | 'light';

const theme = ref<Theme>('dark');

function applyTheme(t: Theme) {
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
    localStorage.setItem('lankford_hub_theme', t);
  }
}

function initTheme() {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('lankford_hub_theme') as Theme | null;
    if (saved === 'dark' || saved === 'light') {
      applyTheme(saved);
    } else {
      applyTheme('dark');
    }
  }
}

// Immediately initialize theme on module evaluation
initTheme();

export function useTheme() {
  const toggleTheme = () => {
    applyTheme(theme.value === 'dark' ? 'light' : 'dark');
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

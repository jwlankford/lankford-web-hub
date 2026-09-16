import { ref, computed } from 'vue';

export interface AuthUserProfile {
  uid: string;
  displayName: string | null;
  email: string | null;
  photoURL: string | null;
}

const currentUser = ref<AuthUserProfile | null>(null);
const isPasskeyAdmin = ref<boolean>(sessionStorage.getItem('academic_admin') === 'true');

export function useAuth() {
  const isAuthenticated = computed(() => currentUser.value !== null || isPasskeyAdmin.value);
  const isAdmin = computed(() => isAuthenticated.value);

  function setPasskeyAdmin(passkey: string) {
    if (passkey) {
      isPasskeyAdmin.value = true;
      sessionStorage.setItem('academic_admin', 'true');
    }
  }

  function logout() {
    currentUser.value = null;
    isPasskeyAdmin.value = false;
    sessionStorage.removeItem('academic_admin');
  }

  return {
    currentUser,
    isAuthenticated,
    isAdmin,
    setPasskeyAdmin,
    logout
  };
}

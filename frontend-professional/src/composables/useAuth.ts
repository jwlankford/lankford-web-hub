import { ref, computed, onMounted } from 'vue';
import { 
  auth, 
  onAuthStateChanged, 
  loginWithGooglePopup, 
  logoutFirebase, 
  type User 
} from '../services/firebase';

export interface AuthUserProfile {
  uid: string;
  displayName: string | null;
  email: string | null;
  photoURL: string | null;
}

const currentUser = ref<AuthUserProfile | null>(null);
const isPasskeyAdmin = ref<boolean>(sessionStorage.getItem('academic_admin') === 'true');
const isAuthLoading = ref<boolean>(true);

export function useAuth() {
  onMounted(() => {
    onAuthStateChanged(auth, (user: User | null) => {
      if (user) {
        currentUser.value = {
          uid: user.uid,
          displayName: user.displayName,
          email: user.email,
          photoURL: user.photoURL
        };
        sessionStorage.setItem('academic_admin', 'true');
      } else {
        currentUser.value = null;
      }
      isAuthLoading.value = false;
    });
  });

  const isAuthenticated = computed(() => currentUser.value !== null || isPasskeyAdmin.value);
  const isAdmin = computed(() => isAuthenticated.value);

  async function loginWithGoogle() {
    isAuthLoading.value = true;
    try {
      const user = await loginWithGooglePopup();
      currentUser.value = {
        uid: user.uid,
        displayName: user.displayName,
        email: user.email,
        photoURL: user.photoURL
      };
      isPasskeyAdmin.value = true;
      sessionStorage.setItem('academic_admin', 'true');
      return { success: true, user };
    } catch (error: any) {
      console.error('Google Sign-In Error:', error);
      return { 
        success: false, 
        message: error.message || 'Failed to sign in with Google. Check Firebase credentials.' 
      };
    } finally {
      isAuthLoading.value = false;
    }
  }

  function setPasskeyAdmin(passkey: string) {
    if (passkey) {
      isPasskeyAdmin.value = true;
      sessionStorage.setItem('academic_admin', 'true');
    }
  }

  async function logout() {
    isAuthLoading.value = true;
    try {
      await logoutFirebase();
    } catch (e) {
      console.warn('Firebase signout warning:', e);
    }
    currentUser.value = null;
    isPasskeyAdmin.value = false;
    sessionStorage.removeItem('academic_admin');
    isAuthLoading.value = false;
  }

  return {
    currentUser,
    isAuthenticated,
    isAdmin,
    isAuthLoading,
    loginWithGoogle,
    setPasskeyAdmin,
    logout
  };
}

// Import the functions you need from the SDKs you need
import { initializeApp, getApps, getApp } from "firebase/app";
import { 
  getAuth, 
  GoogleAuthProvider, 
  signInWithPopup, 
  signOut as firebaseSignOut, 
  onAuthStateChanged,
  type User 
} from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyCg67I7wSA8bVWCiE0mh9z-cyaB7ydEKhQ",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "jeremylankford-add44.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "jeremylankford-add44",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "jeremylankford-add44.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "31318563374",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:31318563374:web:a495f9174887561941ddbf",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "G-Z1WFTD44VK"
};

// Initialize Firebase App & Auth
const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export async function loginWithGooglePopup(): Promise<User> {
  const result = await signInWithPopup(auth, googleProvider);
  return result.user;
}

export async function logoutFirebase(): Promise<void> {
  await firebaseSignOut(auth);
}

export { onAuthStateChanged };
export type { User };
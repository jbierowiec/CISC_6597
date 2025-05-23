// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBU8Fr2JA6laOW5rkNXCX7o0fBxA1Nf0yM",
  authDomain: "worksheets-ai-e3fb8.firebaseapp.com",
  projectId: "worksheets-ai-e3fb8",
  storageBucket: "worksheets-ai-e3fb8.firebasestorage.app",
  messagingSenderId: "398890163026",
  appId: "1:398890163026:web:51d87c8f9d4827cdc0f88b",
  measurementId: "G-LJGB93RP33"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, signInWithPopup, signOut };
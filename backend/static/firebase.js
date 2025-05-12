// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBMW4Em5ro27yTIPw3K2GIAvAbcaSyqCWk",
  authDomain: "simple-project-f8aa7.firebaseapp.com",
  projectId: "simple-project-f8aa7",
  storageBucket: "simple-project-f8aa7.firebasestorage.app",
  messagingSenderId: "678990721209",
  appId: "1:678990721209:web:47d34228ab34b4e5ed2b68",
  measurementId: "G-FSYGN9J7VC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, signInWithPopup };
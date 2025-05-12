const firebaseConfig = {
  apiKey: "AIzaSyBMW4Em5ro27yTIPw3K2GIAvAbcaSyqCWk",
  authDomain: "simple-project-f8aa7.firebaseapp.com",
  projectId: "simple-project-f8aa7",
  storageBucket: "simple-project-f8aa7.firebasestorage.app",
  messagingSenderId: "678990721209",
  appId: "1:678990721209:web:47d34228ab34b4e5ed2b68",
  measurementId: "G-FSYGN9J7VC"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();

function beginLogin(role) {
  auth.signInWithPopup(provider)
    .then(result => {
      const email = result.user.email;

      fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, role })
      })
      .then(res => res.json())
      .then(data => {
        window.location.href = data.redirect;
      })
      .catch(err => {
        alert("Login redirect failed");
        console.error(err);
      });
    })
    .catch(error => {
      console.error("Firebase sign-in error", error);
      alert("Authentication failed.");
    });
}
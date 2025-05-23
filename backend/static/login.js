const firebaseConfig = {
  apiKey: "AIzaSyBU8Fr2JA6laOW5rkNXCX7o0fBxA1Nf0yM",
  authDomain: "worksheets-ai-e3fb8.firebaseapp.com",
  projectId: "worksheets-ai-e3fb8",
  storageBucket: "worksheets-ai-e3fb8.firebasestorage.app",
  messagingSenderId: "398890163026",
  appId: "1:398890163026:web:51d87c8f9d4827cdc0f88b",
  measurementId: "G-LJGB93RP33"
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
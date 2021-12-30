import firebase from 'firebase/compat/app';
import 'firebase/compat/database';

const firebaseConfig = {
  apiKey: "AIzaSyBvy9KIICtW5qR374kCZ8d9TK4Twa8fq-o",
  authDomain: "jarvis-sqri.firebaseapp.com",
  databaseURL: "https://jarvis-sqri-default-rtdb.firebaseio.com",
  projectId: "jarvis-sqri",
  storageBucket: "jarvis-sqri.appspot.com",
  messagingSenderId: "820939342546",
  appId: "1:820939342546:web:c934e0c3a11b5cd8bd630b"
};
// Get a Firestore instance


export const db = firebase
  .initializeApp(firebaseConfig)
  .database()

import config from './env';

import { FirebaseApp } from 'firebase/app';
import { initializeApp } from 'firebase/app';

const firebaseConfig = {
    apiKey: config.firebaseApiKey,
    authDomain: config.firebaseAuthDomain,
    projectId: config.firebaseProjectId,
};

if (!firebaseConfig.apiKey || !firebaseConfig.authDomain || !firebaseConfig.projectId) {
    console.error('Firebase configuration is missing');
}

let app: FirebaseApp;
try {
    app = initializeApp(firebaseConfig);
} catch (error) {
    console.error('Error initializing Firebase:', error);
}

export { app };

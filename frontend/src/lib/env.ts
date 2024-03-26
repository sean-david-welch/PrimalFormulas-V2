const config = {
    baseUrl:
        import.meta.env.VITE_ENVIRONMENT === 'production' ? 'https://api.primalformulas.ie/' : 'http://127.0.0.1:8000/',

    firebaseApiKey: import.meta.env.VITE_FIREBASE_API_KEY,
    firebaseAuthDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
    firebaseProjectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
    firebaseStorageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
    firebaseMessagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
    firebaseAppId: import.meta.env.VITE_FIREBASE_APP_ID,
    firebaseMeasurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,

    stripePublicKey: import.meta.env.VITE_STRIPE_PUBLIC_KEY,
    stripePublicKeyTest: import.meta.env.VITE_TEST_PUBLIC_KEY,
};

export default config;

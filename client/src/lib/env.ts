const config = {
    baseUrl:
        import.meta.env.VITE_ENVIRONMENT === 'production' ? 'https://api.primalformulas.ie/' : 'http://0.0.0.0:80/',

    firebaseApiKey: import.meta.env.VITE_FB_WEB_API_KEY,
    firebaseAuthDomain: import.meta.env.VITE_FB_AUTH_URL,
    firebaseProjectId: import.meta.env.VITE_FB_PROJECT_ID,

    mapsKey: import.meta.env.VITE_PUBLIC_MAPS_KEY,
    recaptchaKey: import.meta.env.VITE_RECAPTCHA_PUBLIC_KEY,

    stripePublicKey: import.meta.env.VITE_STRIPE_PUBLIC_KEY,
    stripePublicKeyTest: import.meta.env.VITE_TEST_PUBLIC_KEY,
};

export default config;

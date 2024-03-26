/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
    theme: {
        extend: {
            screens: {
                md: { max: '896px' },
                lg: { min: '896px' },
            },
        },
        plugins: [],
    },
};

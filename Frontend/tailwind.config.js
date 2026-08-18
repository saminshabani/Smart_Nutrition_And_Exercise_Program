/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eefdf3',
          100: '#d6fae2',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
        },
        accent: {
          500: '#f97316',
        },
      },
      fontFamily: {
        sans: ['Vazirmatn', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

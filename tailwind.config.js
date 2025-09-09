/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        'serif': ['Crimson Text', 'ui-serif', 'Georgia', 'serif'],
      },
      colors: {
        primary: {
          50: '#f0f9f4',
          100: '#daf2e3',
          200: '#b8e5c8',
          300: '#8dd3a6',
          400: '#5cb87e',
          500: '#2ba461',
          600: '#1e854c',
          700: '#18693e',
          800: '#165332',
          900: '#14452a',
        },
        secondary: {
          50: '#fef7ed',
          100: '#fdedd4',
          200: '#fad7a9',
          300: '#f6ba72',
          400: '#f1973a',
          500: '#de6b1a',
          600: '#c75c16',
          700: '#a34715',
          800: '#843a17',
          900: '#6d3016',
        },
      },
    },
  },
  plugins: [],
}

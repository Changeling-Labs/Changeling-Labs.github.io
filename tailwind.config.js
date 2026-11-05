/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './privacy.html'],
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#EEF4FF',
          100: '#DCE9FF',
          200: '#B9D4FF',
          400: '#3D7BE0',
          500: '#0056D2',
          600: '#0048AE',
          700: '#003D93',
          900: '#0F172A',
        },
        turquoise: '#00F5FF',
      },
      boxShadow: {
        card: '0 1px 2px rgba(15, 23, 42, 0.05), 0 8px 24px -12px rgba(15, 23, 42, 0.12)',
      },
    }
  },
  plugins: [],
}

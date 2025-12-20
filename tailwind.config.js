/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './events/templates/**/*.html',
    './users/templates/**/*.html',
    './home/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
        'display': ['Rajdhani', 'sans-serif'],
      },
      colors: {
        space: {
          900: '#0B0C10',
          800: '#1F2833',
          accent: '#66FCF1',
          dim: '#45A29E',
        }
      }
    },
  },
  plugins: [],
}


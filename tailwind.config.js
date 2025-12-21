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
      },
      typography: (theme) => ({
        invert: {
          css: {
            '--tw-prose-body': theme('colors.gray[300]'),
            '--tw-prose-headings': theme('colors.white'),
            '--tw-prose-links': theme('colors.blue[400]'),
            '--tw-prose-bold': theme('colors.white'),
            '--tw-prose-code': theme('colors.yellow[300]'),
            '--tw-prose-pre-bg': 'rgba(0, 0, 0, 0.5)',
            '--tw-prose-quotes': theme('colors.gray[400]'),
            'h1, h2, h3, h4, h5, h6': {
              fontFamily: theme('fontFamily.display'),
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            },
            'h1': {
              borderBottom: `2px solid rgba(249, 115, 22, 0.3)`,
              paddingBottom: '0.3em',
            },
            'h2': {
              borderBottom: `1px solid rgba(249, 115, 22, 0.2)`,
              paddingBottom: '0.3em',
            },
            'h3': {
              color: theme('colors.orange[400]'),
            },
            'code': {
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              border: `1px solid rgba(249, 115, 22, 0.2)`,
              borderRadius: '0.25rem',
              padding: '0.125rem 0.375rem',
            },
            'pre': {
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              border: `1px solid rgba(249, 115, 22, 0.2)`,
            },
            'pre code': {
              backgroundColor: 'transparent',
              border: 'none',
              padding: '0',
            },
            'blockquote': {
              borderLeftColor: theme('colors.orange[500]'),
              backgroundColor: 'rgba(249, 115, 22, 0.05)',
            },
            'th': {
              backgroundColor: 'rgba(249, 115, 22, 0.1)',
              color: theme('colors.orange[400]'),
            },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}


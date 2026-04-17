/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        maersk: {
          dark:    '#00243D',
          blue:    '#0077B6',
          teal:    '#00B4D8',
          light:   '#42B4E6',
          sky:     '#90E0EF',
          pale:    '#CAF0F8',
          bg:      '#F0F4F8',
          card:    '#FFFFFF',
          navy:    '#001D35',
          slate:   '#1E3A5F',
          muted:   '#5B8DB8',
        },
        atlas: {
          green:   '#10B981',
          amber:   '#F59E0B',
          red:     '#EF4444',
          purple:  '#8B5CF6',
          orange:  '#F97316',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-slow':    'pulse 3s cubic-bezier(0.4,0,0.6,1) infinite',
        'fade-in':       'fadeIn 0.5s ease-in-out',
        'slide-up':      'slideUp 0.4s ease-out',
        'slide-right':   'slideRight 0.4s ease-out',
        'glow':          'glow 2s ease-in-out infinite',
        'ticker':        'ticker 30s linear infinite',
        'spin-slow':     'spin 8s linear infinite',
        'bounce-light':  'bounceLight 1s ease-in-out infinite',
        'shimmer':       'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%':   { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)',    opacity: '1' },
        },
        slideRight: {
          '0%':   { transform: 'translateX(-20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)',     opacity: '1' },
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 5px rgba(0,180,216,0.3)'  },
          '50%':      { boxShadow: '0 0 20px rgba(0,180,216,0.7)' },
        },
        ticker: {
          '0%':   { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(-100%)' },
        },
        bounceLight: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':      { transform: 'translateY(-4px)' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition:  '200% 0' },
        },
      },
      backgroundImage: {
        'grid-pattern': "url(\"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%230077B6' fill-opacity='0.05'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
        'ocean-gradient': 'linear-gradient(135deg, #00243D 0%, #003D6B 50%, #0077B6 100%)',
        'card-gradient':  'linear-gradient(135deg, #001D35 0%, #1E3A5F 100%)',
        'teal-gradient':  'linear-gradient(135deg, #00B4D8 0%, #0077B6 100%)',
      }
    },
  },
  plugins: [],
}

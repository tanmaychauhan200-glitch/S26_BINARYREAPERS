/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          darkest: '#07111F',
          dark: '#0B1728',
          card: '#102238',
          border: '#1E3A5F',
          accent: '#38BDF8',
          text: '#E5F0FA',
          muted: '#91A4B8'
        },
        module: {
          river: '#38BDF8',
          wetland: '#2DD4BF',
          forest: '#10B981',
          urban: '#818CF8'
        }
      }
    },
  },
  plugins: [],
}

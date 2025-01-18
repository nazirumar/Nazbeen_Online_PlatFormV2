/** @type {import('tailwindcss').Config} */
module.exports = {
 
  content: [
    './templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ["light", "dark"], // Include desired themes
    darkTheme: "dark", // Default dark theme
  },
};

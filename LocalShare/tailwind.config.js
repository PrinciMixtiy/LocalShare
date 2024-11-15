/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "/templates/**/*.html",
    "./**/templates/**/*.html",
    "./*/templates/**/*.html",
    "./static/**/*.js",
    "./static/**/*.css",
    "./static/**/*/.scss",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

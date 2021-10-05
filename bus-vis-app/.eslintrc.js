module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/airbnb',
  ],
  parserOptions: {
    parser: 'babel-eslint',
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'linebreak-style': 0,
    'max-len': 'off',
    'indent': 'off',
    'comma-dangle': 'off',
    'import/no-extraneous-dependencies': 'off',
    'object-shorthand': 'off',
    'no-plusplus': 'off',
  },
};

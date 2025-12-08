// ESLint v9 flat config
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    ignores: ['node_modules/**'],
    files: ['src/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        console: 'readonly',
        window: 'readonly',
        document: 'readonly',
      },
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-undef': 'error',
      eqeqeq: ['error', 'always'],
      semi: ['error', 'always'],
      quotes: ['error', 'single', { avoidEscape: true }],
      'no-var': 'error',
      'prefer-const': 'warn',
      'no-console': 'off',
    },
  },
];

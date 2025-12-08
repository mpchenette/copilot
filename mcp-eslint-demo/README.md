# MCP ESLint Demo

This directory contains a minimal JavaScript project to demo the ESLint MCP server. It includes one intentionally problematic file (`src/bad.js`) and one clean file (`src/good.js`).

## Setup

```bash
cd mcp-eslint-demo
npm install
```

## Run ESLint

```bash
npm run lint
```

## Auto-fix (where possible)

```bash
npm run lint:fix
```

Use these commands in your MCP setup to point the ESLint server at `mcp-eslint-demo/src`. The errors in `bad.js` demonstrate common rule violations (eqeqeq, semi, quotes, no-var, prefer-const, no-unused-vars, no-undef).

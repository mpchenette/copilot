# Playwright MCP Demo

A minimal static web UI + Playwright tests designed to be easy for an MCP server (e.g., Playwright MCP server) to drive.

## What’s included
- Static UI: `src/index.html`, `src/app.js`, `src/styles.css`
- Playwright tests: `tests/example.spec.ts`
- Scripts: local HTTP server and test runner

## Quick start

1. Install dev dependencies:

```bash
npm install
```

2. Serve the static site (default port 5173):

```bash
npm run serve
```

3. In another terminal, run tests (they assume the server is running):

```bash
npm test
```

To use a different port, set `PORT` when running tests, and start the server on the same port:

```bash
PORT=8080 npm run serve
PORT=8080 npm test
```

## MCP Server Integration Notes
- The page exposes stable selectors (`data-testid`, ids) to enable robust automation.
- Flows covered:
  - Login success/failure
  - Task add/clear
  - Modal open/close
- You can point the Playwright MCP server to the served URL and use actions that mirror the test steps.

## Folder structure
```
playwright-mcp-demo/
  package.json
  README.md
  src/
    index.html
    app.js
    styles.css
  tests/
    example.spec.ts
```

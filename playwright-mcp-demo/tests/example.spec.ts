import { test, expect } from '@playwright/test';

const PORT = process.env.PORT || '5173';
const BASE = `http://localhost:${PORT}`;

// Basic smoke tests for MCP-friendly actions

test.describe('Playwright MCP Demo', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE);
  });

  test('renders title', async ({ page }) => {
    const title = page.getByTestId('title');
    await expect(title).toHaveText('Playwright MCP Demo');
  });

  test('login success and failure', async ({ page }) => {
    await page.fill('#username', 'mcp-user');
    await page.fill('#password', 'secret');
    await page.click('#login-btn');
    await expect(page.locator('#login-status[data-testid="login-success"]')).toContainText('Logged in as mcp-user');

    await page.fill('#username', '');
    await page.fill('#password', '');
    await page.click('#login-btn');
    await expect(page.locator('#login-status[data-testid="login-failed"]')).toHaveText('Login failed');
  });

  test('add and clear tasks', async ({ page }) => {
    await page.fill('#new-task', 'Write MCP test');
    await page.click('#add-task');
    await expect(page.locator('#task-list .task-item .task-text')).toHaveText('Write MCP test');

    await page.check('#task-list .task-item input[type="checkbox"]');
    await page.click('#clear-completed');
    await expect(page.locator('#task-list .task-item')).toHaveCount(0);
  });

  test('modal open/close', async ({ page }) => {
    await page.click('#open-modal');
    const modal = page.locator('dialog#demo-modal');
    await expect(modal).toBeVisible();
    await page.click('#close-modal');
    await expect(modal).not.toBeVisible();
  });

  test('normal user cannot access admin', async ({ page }) => {
    // Login as a normal user
    await page.fill('#username', 'alice');
    await page.fill('#password', 'secret');
    await page.click('#login-btn');
    await expect(page.locator('#login-status[data-testid="login-success"]')).toContainText('Logged in as alice');

    // Navigate to /admin
    await page.goto(`${BASE}/admin`);
    // Confirm access denied message is shown and admin content hidden
    await expect(page.locator('#status[data-testid="admin-access-denied"]')).toHaveText('Access denied: insufficient permissions');
  });

  test('admin can access admin area', async ({ page }) => {
    // Login as admin/admin
    await page.fill('#username', 'admin');
    await page.fill('#password', 'admin');
    await page.click('#login-btn');
    await expect(page.locator('#login-status[data-testid="admin-login"]')).toHaveText('Logged in as admin');

    await page.goto(`${BASE}/admin`);
    await expect(page.locator('#status[data-testid="admin-access-granted"]')).toHaveText('Access granted: admin');
    await expect(page.getByRole('heading', { name: 'System Controls' })).toBeVisible();
  });
});

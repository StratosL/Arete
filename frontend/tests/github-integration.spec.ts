import { test, expect } from '@playwright/test';

test.describe('GitHub Integration Live Test', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should show GitHub input field on upload page', async ({ page }) => {
    // Check if GitHub input field exists
    const githubInput = page.locator('input[placeholder="https://github.com/username"]');
    await expect(githubInput).toBeVisible();
    
    // Check if GitHub label exists
    await expect(page.locator('text=GitHub Profile (Optional)')).toBeVisible();
  });

  test('should show GitHub analysis after resume upload with GitHub URL', async ({ page }) => {
    // Create a test file
    const testFile = Buffer.from('John Doe\nSoftware Engineer\nPython, React, Node.js');
    
    // Fill GitHub URL
    await page.fill('input[placeholder="https://github.com/username"]', 'https://github.com/octocat');
    
    // Upload file
    await page.setInputFiles('input[type="file"]', {
      name: 'test-resume.txt',
      mimeType: 'text/plain',
      buffer: testFile,
    });
    
    // Click upload button
    await page.click('button:has-text("Upload & Parse Resume")');
    
    // Wait for upload to complete (may take time due to LLM processing)
    await expect(page.locator('text=Parsed Resume Data')).toBeVisible({ timeout: 30000 });
    
    // Check if GitHub Analysis section appears
    await expect(page.locator('text=GitHub Analysis')).toBeVisible();
    await expect(page.locator('text=Analyze octocat')).toBeVisible();
  });

  test('should fetch and display GitHub data when analyze button is clicked', async ({ page }) => {
    // Skip upload and directly test GitHub component if it exists
    // This test assumes we can navigate to a state where GitHub analysis is available
    
    // For now, let's test the API endpoint directly through the browser
    const response = await page.request.post('http://localhost:8000/github/analyze', {
      data: { username: 'octocat' }
    });
    
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data.username).toBe('octocat');
    expect(data.impact_metrics.total_repos).toBeGreaterThan(0);
    expect(data.resume_bullet_points).toHaveLength.greaterThan(0);
  });

  test('should handle GitHub analysis errors gracefully', async ({ page }) => {
    // Test with invalid username
    const response = await page.request.post('http://localhost:8000/github/analyze', {
      data: { username: 'this-user-definitely-does-not-exist-12345' }
    });
    
    expect(response.status()).toBe(404);
  });
});
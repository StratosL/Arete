import { test, expect } from '@playwright/test';
import path from 'path';

test('complete resume optimization workflow', async ({ page }) => {
  // Navigate to app
  await page.goto('/');
  await expect(page.getByText('Upload Your Resume')).toBeVisible();

  // Upload resume
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(path.join(__dirname, 'fixtures', 'sample-resume.pdf'));
  
  await page.getByRole('button', { name: /upload & parse resume/i }).click();
  
  // Wait for parsing to complete
  await expect(page.getByText('Parsed Resume Data')).toBeVisible({ timeout: 30000 });
  await expect(page.getByText('John Doe')).toBeVisible();

  // Enter job description
  await page.getByPlaceholder('Paste the job description here...').fill(
    'Software Engineer position requiring Python, FastAPI, and React experience. ' +
    '3+ years of development experience required. Must have experience with databases and cloud platforms.'
  );
  
  await page.getByRole('button', { name: /analyze job description/i }).click();
  
  // Wait for job analysis
  await expect(page.getByText('Job Analysis Results')).toBeVisible({ timeout: 30000 });
  await expect(page.getByText('Software Engineer')).toBeVisible();

  // Start optimization
  await page.getByRole('button', { name: /start optimization/i }).click();
  
  // Wait for optimization to complete
  await expect(page.getByText('Optimization complete!')).toBeVisible({ timeout: 30000 });
  await expect(page.getByText('Optimization Suggestions')).toBeVisible();

  // Download PDF
  const downloadPromise = page.waitForDownload();
  await page.getByRole('button', { name: /pdf format/i }).click();
  const download = await downloadPromise;
  
  expect(download.suggestedFilename()).toMatch(/\.pdf$/);
});
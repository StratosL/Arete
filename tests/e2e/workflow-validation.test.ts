import { test, expect } from '@playwright/test';

test.describe('Complete User Workflow E2E', () => {
  test('full journey: upload → analyze → optimize → export', async ({ page }) => {
    const startTime = Date.now();
    
    // Navigate to app
    await page.goto('/');
    
    // 1. UPLOAD WORKFLOW
    console.log('Testing upload workflow...');
    const uploadStart = Date.now();
    
    await page.setInputFiles('input[type="file"]', 'tests/fixtures/sample-resume.pdf');
    await page.fill('input[placeholder*="github"]', 'https://github.com/testuser');
    await page.click('button:has-text("Upload & Parse Resume")');
    
    // Wait for parsing completion
    await expect(page.locator('text=Personal Information')).toBeVisible({ timeout: 45000 });
    const uploadTime = Date.now() - uploadStart;
    console.log(`Upload completed in ${uploadTime}ms`);
    
    // 2. JOB ANALYSIS WORKFLOW  
    console.log('Testing job analysis workflow...');
    const analysisStart = Date.now();
    
    await page.fill('textarea[placeholder*="job description"]', 
      'Senior Software Engineer position requiring Python, React, and 5+ years experience');
    await page.click('button:has-text("Analyze Job Description")');
    
    await expect(page.locator('text=Job Analysis Results')).toBeVisible({ timeout: 30000 });
    const analysisTime = Date.now() - analysisStart;
    console.log(`Analysis completed in ${analysisTime}ms`);
    
    // 3. OPTIMIZATION WORKFLOW
    console.log('Testing optimization workflow...');
    const optimizationStart = Date.now();
    
    await page.click('button:has-text("Start Optimization")');
    await expect(page.locator('text=Optimization Suggestions')).toBeVisible({ timeout: 70000 });
    
    // Select first suggestion
    await page.click('button:has-text("Select this")').first();
    await page.click('button:has-text("Apply Selected")');
    
    const optimizationTime = Date.now() - optimizationStart;
    console.log(`Optimization completed in ${optimizationTime}ms`);
    
    // 4. EXPORT WORKFLOW
    console.log('Testing export workflow...');
    const exportStart = Date.now();
    
    await page.click('button:has-text("PDF Format")');
    
    const exportTime = Date.now() - exportStart;
    console.log(`Export completed in ${exportTime}ms`);
    
    const totalTime = Date.now() - startTime;
    console.log(`Total workflow time: ${totalTime}ms`);
    
    // Validate performance thresholds
    expect(uploadTime).toBeLessThan(45000); // 45s max
    expect(analysisTime).toBeLessThan(35000); // 35s max  
    expect(optimizationTime).toBeLessThan(75000); // 75s max
    expect(exportTime).toBeLessThan(15000); // 15s max
  });

  test('template selection workflow', async ({ page }) => {
    await page.goto('/');
    
    // Upload resume first
    await page.setInputFiles('input[type="file"]', 'tests/fixtures/sample-resume.pdf');
    await page.click('button:has-text("Upload & Parse Resume")');
    await expect(page.locator('text=Personal Information')).toBeVisible({ timeout: 45000 });
    
    // Navigate to export
    await page.click('text=Export');
    
    // Test template switching
    await expect(page.locator('text=ATS Classic')).toBeVisible();
    await expect(page.locator('text=Modern Professional')).toBeVisible();
    
    // Switch to modern template
    await page.click('text=Modern Professional');
    await expect(page.locator('.border-blue-500')).toBeVisible();
    
    // Test export with modern template
    await page.click('button:has-text("PDF Format")');
    
    // Should open new tab for print dialog
    const [newPage] = await Promise.all([
      page.waitForEvent('popup'),
      page.click('button:has-text("PDF Format")')
    ]);
    
    expect(newPage).toBeTruthy();
  });

  test('error handling scenarios', async ({ page }) => {
    await page.goto('/');
    
    // Test invalid file upload
    await page.click('button:has-text("Upload & Parse Resume")');
    await expect(page.locator('text=Please select a file')).toBeVisible();
    
    // Test invalid job analysis
    await page.fill('textarea[placeholder*="job description"]', 'short');
    await page.click('button:has-text("Analyze Job Description")');
    await expect(page.locator('text=minimum 50 characters')).toBeVisible();
    
    // Test network error simulation
    await page.route('**/resume/upload', route => route.abort());
    await page.setInputFiles('input[type="file"]', 'tests/fixtures/sample-resume.pdf');
    await page.click('button:has-text("Upload & Parse Resume")');
    await expect(page.locator('text=failed')).toBeVisible({ timeout: 10000 });
  });
});
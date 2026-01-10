# E2E Test Fixtures

This directory contains test files used by Playwright E2E tests.

## Required Files

### `sample-resume.pdf`
A sample PDF resume file for testing upload functionality. Should contain:
- Personal information (name, email, phone)
- Work experience with job titles and descriptions
- Technical skills section
- Education information

**To add this file:**
1. Create or find a sample PDF resume
2. Save it as `sample-resume.pdf` in this directory
3. Ensure it contains realistic resume content for testing

### `sample-job-description.txt` (Optional)
A sample job description for testing job analysis functionality.

## File Requirements
- Files should be realistic but not contain real personal information
- PDF files should be under 10MB (application limit)
- Content should include technical skills that match the application's target use case

## Usage
These files are automatically used by the E2E tests in `complete-workflow.spec.ts`.
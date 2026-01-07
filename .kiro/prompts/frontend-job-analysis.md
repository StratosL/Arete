Using React 18 + TypeScript 2024-2025 best practices as context, implement job description input component for Arete.

Documentation to read:
- READ: api-contracts.yaml (JobAnalysis request/response)
- READ: frontend/src/components/ResumeUpload.tsx (existing patterns)
- READ: frontend/src/lib/api.ts (API client patterns)

Focus on: react-hook-form + Controller, Zod validation, shadcn/ui Field components, dual input modes (text/URL)

First, install dependencies:
```bash
cd frontend && npm install react-hook-form @hookform/resolvers zod
```

Then create/modify these files:

1. frontend/src/components/JobDescriptionInput.tsx with:
   - Dual input modes using Tabs (text input vs URL input)
   - react-hook-form with Controller pattern
   - Zod schema validation (min 50 chars for text, valid URL)
   - Loading states and error handling with ErrorBoundary
   - shadcn/ui Field components with data-invalid props
   
   Example pattern:
   ```tsx
   <Tabs defaultValue="text">
     <TabsList><TabsTrigger value="text">Text</TabsTrigger></TabsList>
     <TabsContent value="text">
       <Controller name="job_text" control={form.control} render={...} />
     </TabsContent>
   </Tabs>
   ```

2. frontend/src/types/index.ts with:
   - JobAnalysisRequest and JobAnalysis interfaces
   - Form validation types matching Zod schemas

3. frontend/src/lib/api.ts with:
   - analyzeJob(data: JobAnalysisRequest) async function
   - Proper error handling and response typing

4. UPDATE frontend/src/App.tsx:
   - Add JobDescriptionInput component after ResumeDisplay
   - Pass resume data context for integration
   - Handle job analysis results state

Test requirements:

Unit tests (no external dependencies):
- Test form validation (text length, URL format)
- Test component rendering and state changes
- Expected: 4 tests passing

Integration tests (with API):
- Test job analysis submission and response handling
- Mark with @jest.mark.integration
- Expected: 2 tests passing

E2E/Manual testing:
- Text input: Enter job description, submit, see analysis results
- URL input: Enter job URL, submit, see scraped and analyzed results
- Validation: Test empty inputs, invalid URLs show proper errors

All linting (npm run lint, npm run type-check) must pass

When everything is green, let the user know we are ready to commit

Output format:
Summary: [what was accomplished]
Files created/modified: [list]
Components: [list with descriptions]

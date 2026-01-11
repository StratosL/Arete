# 0011. Optimization Persistence

**Date**: 2025-01-10
**Status**: Accepted
**Tags**: architecture, database, api, optimization

## Context

This document explains the optimization persistence feature that allows saving AI optimization results and using them in document exports.

## Problem

Previously, the AI optimization service generated suggestions via SSE streaming but never persisted them. The export service always used the original `parsed_data` from the database, so users couldn't export their optimized resumes.

## Solution

1. **Added `optimized_data` field** to resume storage
2. **Created `/optimize/save` endpoint** to persist optimization results  
3. **Updated export service** to check for optimized data first, falling back to original data

## Setup Steps

### 1. Run Database Migration

Add the `optimized_data` column to your resumes table:

```bash
# Option 1: Run migration script
cd backend
pip install supabase python-dotenv
python ../scripts/database/add_optimized_data_column.py

# Option 2: Manual SQL (in Supabase SQL Editor)
ALTER TABLE resumes ADD COLUMN IF NOT EXISTS optimized_data JSONB;
```

### 2. Test the Implementation

```bash
# Run the test script to verify everything works
python scripts/validation/test_optimization_persistence.py
```

### 3. Frontend Integration

The frontend needs to call the new save endpoint after users apply optimizations:

```javascript
// After user applies optimization suggestions
const response = await fetch('/optimize/save', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_id: resumeId,
    optimized_data: updatedResumeData
  })
});
```

## API Changes

### New Endpoint: `POST /optimize/save`

**Request:**
```json
{
  "resume_id": "uuid",
  "optimized_data": {
    "id": "uuid",
    "personal_info": { ... },
    "experience": [ ... ],
    "skills": { ... },
    "projects": [ ... ],
    "education": [ ... ]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Optimization saved"
}
```

### Updated Export Behavior

The export endpoints (`/export/pdf` and `/export/docx`) now:

1. **First check** for `optimized_data` in the database
2. **Fall back** to `parsed_data` if no optimized version exists
3. **Generate documents** using the appropriate data

## Database Schema

The `resumes` table now includes:

```sql
CREATE TABLE resumes (
  id UUID PRIMARY KEY,
  user_id UUID,
  filename TEXT,
  file_path TEXT,
  parsed_data JSONB,      -- Original parsed resume data
  optimized_data JSONB,   -- NEW: AI-optimized resume data
  status TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## Workflow

1. **Upload Resume** → `parsed_data` stored
2. **Run Optimization** → Suggestions generated via SSE
3. **Apply Suggestions** → Frontend calls `/optimize/save` with `optimized_data`
4. **Export Resume** → Uses `optimized_data` if available, otherwise `parsed_data`

This ensures users can export their optimized resumes while maintaining backward compatibility with existing data.
-- Manual Database Migration Required
-- Run this SQL in your Supabase SQL Editor:

ALTER TABLE resumes ADD COLUMN IF NOT EXISTS optimized_data JSONB;

-- This adds the optimized_data column to store AI optimization results
-- The column will be NULL for resumes that haven't been optimized
-- Export service will use optimized_data when available, fallback to parsed_data

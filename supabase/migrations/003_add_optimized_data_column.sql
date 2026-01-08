-- Add optimized_data column to resumes table
-- This stores AI optimization results applied by users

ALTER TABLE resumes ADD COLUMN IF NOT EXISTS optimized_data JSONB;

-- Add comment for documentation
COMMENT ON COLUMN resumes.optimized_data IS 'Stores AI-optimized resume data when user applies suggestions. NULL if no optimizations applied.';

-- Temporarily disable RLS for MVP development
-- This allows the application to work without authentication
-- TODO: Re-enable RLS when authentication is implemented

ALTER TABLE resumes DISABLE ROW LEVEL SECURITY;
ALTER TABLE jobs DISABLE ROW LEVEL SECURITY;
ALTER TABLE optimizations DISABLE ROW LEVEL SECURITY;

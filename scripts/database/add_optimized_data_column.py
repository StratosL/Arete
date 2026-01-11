#!/usr/bin/env python3
"""
Migration script to add optimized_data column to resumes table.
Run this once to update the database schema.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_service_key:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
        return
    
    # Create Supabase client with service key (admin privileges)
    supabase = create_client(supabase_url, supabase_service_key)
    
    try:
        # Add optimized_data column to resumes table
        sql = """
        ALTER TABLE resumes 
        ADD COLUMN IF NOT EXISTS optimized_data JSONB;
        """
        
        result = supabase.rpc('exec_sql', {'sql': sql}).execute()
        print("✅ Successfully added optimized_data column to resumes table")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("Note: You may need to run this SQL manually in Supabase SQL Editor:")
        print("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS optimized_data JSONB;")

if __name__ == "__main__":
    main()
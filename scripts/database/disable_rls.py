#!/usr/bin/env python3
"""
Quick script to disable RLS for MVP development
"""

import os
import sys

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: python-dotenv not installed")
    sys.exit(1)

try:
    from supabase import create_client
    
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: Missing Supabase credentials")
        sys.exit(1)
    
    supabase = create_client(url, service_key)
    
    # Disable RLS for MVP
    sql = """
    ALTER TABLE resumes DISABLE ROW LEVEL SECURITY;
    ALTER TABLE jobs DISABLE ROW LEVEL SECURITY;
    ALTER TABLE optimizations DISABLE ROW LEVEL SECURITY;
    """
    
    supabase.rpc("exec_sql", {"sql": sql})
    print("✅ RLS disabled for MVP development")
    
except Exception as e:
    print(f"❌ Failed to disable RLS: {str(e)}")
    sys.exit(1)

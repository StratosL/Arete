#!/usr/bin/env python3
"""
Database Schema Verification Script
Ensures all required columns exist for new deployments
"""

import os
import sys
from supabase import create_client

def verify_schema():
    """Verify database schema has all required columns"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
        return False
    
    supabase = create_client(url, service_key)
    
    try:
        # Check if optimized_data column exists
        result = supabase.rpc("exec_sql", {
            "sql": """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'resumes' 
                AND column_name = 'optimized_data';
            """
        })
        
        if result.data:
            print("✅ Database schema is complete - optimized_data column exists")
            return True
        else:
            print("❌ Missing optimized_data column - run migrations")
            return False
            
    except Exception as e:
        print(f"❌ Schema verification failed: {e}")
        return False

if __name__ == "__main__":
    if verify_schema():
        print("🎉 Database ready for optimization persistence!")
    else:
        print("🔧 Run setup script to apply missing migrations")
        sys.exit(1)

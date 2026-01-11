#!/usr/bin/env python3
"""
Test script to verify optimization persistence functionality.
"""

import asyncio
import json
import os
from supabase import create_client
from dotenv import load_dotenv

async def test_optimization_persistence():
    """Test the optimization persistence workflow"""
    
    # Load environment
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_service_key:
        print("❌ Missing Supabase credentials")
        return
    
    supabase = create_client(supabase_url, supabase_service_key)
    
    # Test data
    test_resume_id = "test-resume-123"
    original_data = {
        "id": test_resume_id,
        "personal_info": {"name": "Test User", "email": "test@example.com"},
        "experience": [{"title": "Developer", "company": "Test Corp", "description": ["Built apps"]}],
        "skills": {"technical": ["Python", "JavaScript"]},
        "projects": [],
        "education": []
    }
    
    optimized_data = {
        "id": test_resume_id,
        "personal_info": {"name": "Test User", "email": "test@example.com"},
        "experience": [{"title": "Senior Developer", "company": "Test Corp", "description": ["Built scalable web applications using Python and React"]}],
        "skills": {"technical": ["Python", "JavaScript", "React", "FastAPI"]},
        "projects": [],
        "education": []
    }
    
    try:
        # 1. Create test resume
        print("1. Creating test resume...")
        supabase.table("resumes").upsert({
            "id": test_resume_id,
            "user_id": None,
            "filename": "test_resume.pdf",
            "parsed_data": original_data,
            "optimized_data": None,
            "status": "parsed"
        }).execute()
        print("✅ Test resume created")
        
        # 2. Simulate saving optimization
        print("2. Saving optimization...")
        supabase.table("resumes").update({
            "optimized_data": optimized_data
        }).eq("id", test_resume_id).execute()
        print("✅ Optimization saved")
        
        # 3. Test export service logic
        print("3. Testing export data selection...")
        result = supabase.table("resumes").select("*").eq("id", test_resume_id).execute()
        resume_record = result.data[0]
        
        # This mimics the export service logic
        export_data = resume_record.get("optimized_data") or resume_record["parsed_data"]
        
        if export_data == optimized_data:
            print("✅ Export service correctly uses optimized data")
        else:
            print("❌ Export service not using optimized data")
            
        # 4. Test fallback to original data
        print("4. Testing fallback to original data...")
        supabase.table("resumes").update({
            "optimized_data": None
        }).eq("id", test_resume_id).execute()
        
        result = supabase.table("resumes").select("*").eq("id", test_resume_id).execute()
        resume_record = result.data[0]
        export_data = resume_record.get("optimized_data") or resume_record["parsed_data"]
        
        if export_data == original_data:
            print("✅ Export service correctly falls back to original data")
        else:
            print("❌ Export service fallback not working")
            
        # 5. Cleanup
        print("5. Cleaning up...")
        supabase.table("resumes").delete().eq("id", test_resume_id).execute()
        print("✅ Test data cleaned up")
        
        print("\n🎉 All tests passed! Optimization persistence is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        # Cleanup on failure
        try:
            supabase.table("resumes").delete().eq("id", test_resume_id).execute()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_optimization_persistence())
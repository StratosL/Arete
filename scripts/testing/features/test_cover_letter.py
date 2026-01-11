#!/usr/bin/env python3
"""
Test script to verify the cover letter endpoint is working
"""
import requests
import json

def test_cover_letter_endpoint():
    """Test the cover letter generation endpoint"""
    
    # Test data
    test_data = {
        "resume_id": "test-resume-id",
        "job_id": "test-job-id"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/optimize/cover-letter",
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Cover letter generated:")
            print(f"Length: {len(data.get('cover_letter', ''))}")
            print(f"Generated at: {data.get('generated_at')}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    test_cover_letter_endpoint()
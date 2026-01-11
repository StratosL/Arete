#!/usr/bin/env python3
"""
Quick GitHub API check - minimal test
"""
import requests

def quick_check():
    try:
        # Test GitHub service endpoint
        response = requests.post(
            "http://localhost:8000/github/analyze",
            json={"username": "octocat"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GitHub API works - {data.get('username')} has {data.get('impact_metrics', {}).get('total_repos', 0)} repos")
            return True
        else:
            print(f"❌ API returned {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_check()
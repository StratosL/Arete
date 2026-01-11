#!/usr/bin/env python3
import requests
import json

def test_github_endpoint():
    print("Testing GitHub endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:8000/github/analyze",
            json={"username": "octocat"},
            timeout=60  # Longer timeout
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"Username: {data['username']}")
            print(f"Repos: {data['impact_metrics']['total_repos']}")
            print(f"Stars: {data['impact_metrics']['total_stars']}")
            print(f"Languages: {data['tech_stack']['primary_languages'][:3]}")
            print(f"Bullet points: {len(data['resume_bullet_points'])}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    test_github_endpoint()
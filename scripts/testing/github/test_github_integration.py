#!/usr/bin/env python3
"""
Live test of GitHub integration API endpoint
"""
import requests
import json
import sys

def test_github_api_endpoint():
    """Test the GitHub analysis endpoint directly"""
    print("🔍 Testing GitHub API endpoint...")
    
    # Test with a real GitHub username
    test_username = "octocat"  # GitHub's mascot account
    
    try:
        response = requests.post(
            "http://localhost:8000/github/analyze",
            json={"username": test_username},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ GitHub API endpoint working!")
            print(f"Username: {data.get('username')}")
            print(f"Total Repos: {data.get('impact_metrics', {}).get('total_repos', 0)}")
            print(f"Total Stars: {data.get('impact_metrics', {}).get('total_stars', 0)}")
            print(f"Top Languages: {data.get('tech_stack', {}).get('primary_languages', [])[:3]}")
            print(f"Resume Bullets: {len(data.get('resume_bullet_points', []))}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("Make sure the backend is running with: docker-compose up")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_github_service_imports():
    """Test if GitHub service can be imported and has required methods"""
    print("\n🔍 Testing GitHub service imports...")
    
    try:
        # Test if we can import the service
        import sys
        sys.path.append('backend')
        
        from app.github.service import github_service
        
        # Check if required methods exist
        required_methods = [
            'analyze_github_profile',
            '_fetch_user_data', 
            '_fetch_user_repositories',
            '_calculate_impact_metrics'
        ]
        
        for method in required_methods:
            if hasattr(github_service, method):
                print(f"✅ {method} exists")
            else:
                print(f"❌ {method} missing")
                return False
                
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 GitHub Integration Live Test\n")
    
    # Test 1: Service imports
    service_ok = test_github_service_imports()
    
    # Test 2: API endpoint
    api_ok = test_github_api_endpoint()
    
    print(f"\n📊 Test Results:")
    print(f"Service Import: {'✅' if service_ok else '❌'}")
    print(f"API Endpoint: {'✅' if api_ok else '❌'}")
    
    if service_ok and api_ok:
        print("\n🎉 GitHub integration is working!")
        sys.exit(0)
    else:
        print("\n💥 GitHub integration has issues!")
        sys.exit(1)
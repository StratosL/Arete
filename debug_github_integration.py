#!/usr/bin/env python3
"""
GitHub Integration Diagnostic Script
Run this to debug GitHub integration issues
"""

import requests
import json
import subprocess
import sys
from pathlib import Path

def print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def test_backend_github_api():
    """Test if backend GitHub API endpoint is working"""
    print_section("1. Backend GitHub API Test")
    
    try:
        # Test with a known GitHub user
        response = requests.post(
            "http://localhost:8000/github/analyze",
            json={"username": "octocat"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ GitHub API endpoint is working")
            print(f"Sample response keys: {list(data.keys())}")
            return True
        else:
            print(f"❌ GitHub API failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend (http://localhost:8000)")
        print("   Make sure backend is running: docker-compose up")
        return False
    except Exception as e:
        print(f"❌ GitHub API test failed: {e}")
        return False

def test_frontend_components():
    """Check if frontend GitHub components exist"""
    print_section("2. Frontend Components Check")
    
    github_component = Path("frontend/src/components/GitHubAnalysis.tsx")
    
    if github_component.exists():
        print("✅ GitHubAnalysis.tsx exists")
        
        # Check if component has key methods
        content = github_component.read_text()
        if "analyzeGitHub" in content:
            print("✅ analyzeGitHub function found")
        else:
            print("❌ analyzeGitHub function missing")
            
        if "github/analyze" in content:
            print("✅ API endpoint call found")
        else:
            print("❌ API endpoint call missing")
            
        return True
    else:
        print("❌ GitHubAnalysis.tsx not found")
        return False

def test_resume_upload_integration():
    """Test resume upload with GitHub URL"""
    print_section("3. Resume Upload + GitHub Integration Test")
    
    # Create a minimal test resume file
    test_resume = Path("test_resume.txt")
    test_resume.write_text("""
John Doe
Software Engineer
john@example.com

Experience:
- Senior Developer at TechCorp (2020-2023)
- Built web applications with Python and React

Skills:
- Python, JavaScript, React, FastAPI
- Git, Docker, AWS
""")
    
    try:
        # Test resume upload with GitHub URL
        with open(test_resume, 'rb') as f:
            files = {'file': f}
            data = {'github_url': 'https://github.com/octocat'}
            
            response = requests.post(
                "http://localhost:8000/resume/upload",
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume upload successful")
            print(f"Resume ID: {result.get('id', 'N/A')}")
            
            # Check if GitHub URL was stored
            if result.get('data', {}).get('personal_info', {}).get('github'):
                print("✅ GitHub URL processed in resume")
            else:
                print("⚠️  GitHub URL not found in parsed resume")
                
            return True, result.get('id')
        else:
            print(f"❌ Resume upload failed: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Resume upload test failed: {e}")
        return False, None
    finally:
        # Clean up test file
        if test_resume.exists():
            test_resume.unlink()

def test_frontend_github_flow():
    """Test if frontend can handle GitHub analysis"""
    print_section("4. Frontend GitHub Flow Test")
    
    # Check if frontend is running
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running")
        else:
            print(f"⚠️  Frontend returned status {response.status_code}")
    except:
        print("❌ Frontend not accessible at http://localhost:3000")
        print("   Make sure frontend is running: cd frontend && npm run dev")
        return False
    
    # Check browser console for errors (manual step)
    print("\n📋 Manual Frontend Test Steps:")
    print("1. Open http://localhost:3000 in browser")
    print("2. Upload a resume with GitHub URL")
    print("3. Check browser console (F12) for errors")
    print("4. Look for GitHub Analysis section after upload")
    
    return True

def generate_curl_test():
    """Generate curl commands for manual testing"""
    print_section("5. Manual Curl Tests")
    
    print("Test GitHub API directly:")
    print('curl -X POST http://localhost:8000/github/analyze \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"username": "octocat"}\'')
    
    print("\nTest resume upload with GitHub:")
    print('curl -X POST http://localhost:8000/resume/upload \\')
    print('  -F "file=@your_resume.pdf" \\')
    print('  -F "github_url=https://github.com/yourusername"')

def main():
    print("🔍 GitHub Integration Diagnostic Tool")
    print("This will test the GitHub integration end-to-end")
    
    results = {}
    
    # Run all tests
    results['backend_api'] = test_backend_github_api()
    results['frontend_components'] = test_frontend_components()
    results['resume_upload'], resume_id = test_resume_upload_integration()
    results['frontend_flow'] = test_frontend_github_flow()
    
    generate_curl_test()
    
    # Generate report
    print_section("DIAGNOSTIC REPORT")
    
    print("Test Results:")
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test}: {status}")
    
    # Diagnosis
    print("\n🔍 DIAGNOSIS:")
    
    if not results['backend_api']:
        print("❌ Backend GitHub API is not working")
        print("   - Check if backend container is running")
        print("   - Check GitHub API route in backend/app/github/routes.py")
        print("   - Verify GitHub service implementation")
        
    elif not results['frontend_components']:
        print("❌ Frontend GitHub components missing or broken")
        print("   - Check frontend/src/components/GitHubAnalysis.tsx")
        print("   - Verify component is imported in main app")
        
    elif not results['resume_upload']:
        print("❌ Resume upload with GitHub URL failing")
        print("   - Check resume upload endpoint")
        print("   - Verify GitHub URL processing in parser")
        
    elif not results['frontend_flow']:
        print("❌ Frontend not accessible")
        print("   - Start frontend: cd frontend && npm run dev")
        print("   - Check for JavaScript errors in browser console")
        
    else:
        print("✅ All backend tests pass - issue likely in frontend UI")
        print("   - Check browser console for JavaScript errors")
        print("   - Verify GitHubAnalysis component is rendered")
        print("   - Check if GitHub section appears after resume upload")
    
    print(f"\n📊 Overall Status: {'✅ HEALTHY' if all(results.values()) else '❌ ISSUES FOUND'}")

if __name__ == "__main__":
    main()
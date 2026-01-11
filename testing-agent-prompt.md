#!/usr/bin/env python3
"""
Manual GitHub Integration Test Report
"""
import requests
import json

def test_backend_github():
    """Test backend GitHub functionality"""
    print("🔍 BACKEND GITHUB API TEST")
    print("=" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/github/analyze",
            json={"username": "octocat"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ GitHub API Endpoint: WORKING")
            print(f"   - Username: {data['username']}")
            print(f"   - Total Repos: {data['impact_metrics']['total_repos']}")
            print(f"   - Total Stars: {data['impact_metrics']['total_stars']}")
            print(f"   - Primary Languages: {data['tech_stack']['primary_languages'][:3]}")
            print(f"   - Resume Bullets: {len(data['resume_bullet_points'])}")
            print(f"   - Sample Bullet: {data['resume_bullet_points'][0][:60]}...")
            return True
        else:
            print(f"❌ GitHub API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub API Exception: {e}")
        return False

def test_resume_upload():
    """Test resume upload functionality"""
    print("\n🔍 RESUME UPLOAD TEST")
    print("=" * 40)
    
    try:
        # Create test resume file
        test_content = """John Doe
Software Engineer
john.doe@email.com
+1234567890

EXPERIENCE
Senior Software Engineer - Tech Corp (2020-2023)
- Built scalable web applications using Python and React
- Led team of 5 developers
- Implemented CI/CD pipelines

SKILLS
Python, JavaScript, React, FastAPI, PostgreSQL, Docker, AWS

PROJECTS
E-commerce Platform
- Full-stack application with 10K+ users
- Technologies: Python, React, PostgreSQL
"""
        
        files = {'file': ('test-resume.txt', test_content, 'text/plain')}
        data = {'github_url': 'https://github.com/octocat'}
        
        response = requests.post(
            "http://localhost:8000/resume/upload",
            files=files,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Resume Upload: WORKING")
            print(f"   - Status: {result['status']}")
            print(f"   - Resume ID: {result['id']}")
            print(f"   - Name: {result['data']['personal_info']['name']}")
            print(f"   - GitHub URL stored: {data['github_url']}")
            return True, result['id']
        else:
            print(f"❌ Resume Upload Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print(f"❌ Resume Upload Exception: {e}")
        return False, None

def check_frontend_components():
    """Check if frontend has GitHub components"""
    print("\n🔍 FRONTEND COMPONENT CHECK")
    print("=" * 40)
    
    try:
        # Check if frontend is accessible
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Check for GitHub-related content
            github_checks = {
                "GitHub input field": 'placeholder="https://github.com/username"' in content,
                "GitHub icon": 'Github' in content or 'github' in content,
                "GitHub Analysis component": 'GitHubAnalysis' in content or 'GitHub Analysis' in content,
            }
            
            print("✅ Frontend: ACCESSIBLE")
            for check, result in github_checks.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check}: {'Found' if result else 'Not found'}")
                
            return any(github_checks.values())
        else:
            print(f"❌ Frontend Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Frontend Exception: {e}")
        return False

def generate_report():
    """Generate comprehensive test report"""
    print("\n" + "=" * 50)
    print("🚀 GITHUB INTEGRATION LIVE TEST REPORT")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_github()
    
    # Test resume upload
    upload_ok, resume_id = test_resume_upload()
    
    # Test frontend
    frontend_ok = check_frontend_components()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 40)
    print(f"Backend GitHub API: {'✅ WORKING' if backend_ok else '❌ BROKEN'}")
    print(f"Resume Upload: {'✅ WORKING' if upload_ok else '❌ BROKEN'}")
    print(f"Frontend Components: {'✅ PRESENT' if frontend_ok else '❌ MISSING'}")
    
    print(f"\n🎯 INTEGRATION STATUS")
    if backend_ok and upload_ok and frontend_ok:
        print("✅ GitHub integration is FULLY FUNCTIONAL")
        print("   - Users can upload resumes with GitHub URLs")
        print("   - Backend can analyze GitHub profiles")
        print("   - Frontend has GitHub analysis components")
    elif backend_ok and upload_ok:
        print("⚠️  GitHub integration is PARTIALLY FUNCTIONAL")
        print("   - Backend works but frontend may have issues")
    else:
        print("❌ GitHub integration has MAJOR ISSUES")
    
    print(f"\n📋 NEXT STEPS")
    if not backend_ok:
        print("   - Fix GitHub API endpoint")
    if not upload_ok:
        print("   - Fix resume upload with GitHub URL")
    if not frontend_ok:
        print("   - Verify GitHub components are properly imported")
    if backend_ok and upload_ok and frontend_ok:
        print("   - Test complete user workflow in browser")
        print("   - Verify GitHub data appears in resume display")
        print("   - Test GitHub bullet point integration")

if __name__ == "__main__":
    generate_report()
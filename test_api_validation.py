#!/usr/bin/env python3
"""
Backend API Validation Script
Tests all endpoints systematically for API contract compliance and error handling.
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

class APIValidator:
    def __init__(self):
        self.results = {}
        self.test_data = {}
    
    def log_result(self, endpoint: str, status: str, details: str = ""):
        """Log test result"""
        self.results[endpoint] = {"status": status, "details": details}
        print(f"{'✅' if status == 'PASS' else '❌'} {endpoint}: {status}")
        if details:
            print(f"   {details}")
    
    def test_health_endpoint(self):
        """Test basic health endpoint"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_result("/health", "PASS", "Health check successful")
                    return True
                else:
                    self.log_result("/health", "FAIL", f"Invalid response: {data}")
            else:
                self.log_result("/health", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("/health", "FAIL", f"Connection error: {e}")
        return False
    
    def test_resume_upload(self):
        """Test /resume/upload endpoint"""
        try:
            # Use the text resume file we created
            with open("test_resume.txt", "rb") as f:
                test_content = f.read()
            
            files = {"file": ("test_resume.txt", test_content, "text/plain")}
            data = {"github_url": "https://github.com/testuser"}
            
            response = requests.post(f"{BASE_URL}/resume/upload", files=files, data=data, timeout=TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                required_fields = ["id", "status", "message", "data"]
                if all(field in result for field in required_fields):
                    if result["data"] and "id" in result["data"]:
                        self.test_data["resume_id"] = result["data"]["id"]
                        self.log_result("/resume/upload", "PASS", f"Resume uploaded: {result['id']}")
                        return True
                    else:
                        self.log_result("/resume/upload", "FAIL", "Missing data.id in response")
                else:
                    self.log_result("/resume/upload", "FAIL", f"Missing fields: {set(required_fields) - set(result.keys())}")
            else:
                self.log_result("/resume/upload", "FAIL", f"Status: {response.status_code}, Body: {response.text[:200]}")
        except Exception as e:
            self.log_result("/resume/upload", "FAIL", f"Error: {e}")
        return False
    
    def test_jobs_analyze(self):
        """Test /jobs/analyze endpoint"""
        try:
            # Test with job text
            payload = {
                "job_text": "Senior Software Engineer position requiring Python, FastAPI, React, and 5+ years experience. Must have experience with cloud platforms and microservices architecture."
            }
            
            response = requests.post(f"{BASE_URL}/jobs/analyze", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                required_fields = ["id", "title", "company", "required_skills", "preferred_skills", "technologies", "experience_level", "key_requirements"]
                if all(field in result for field in required_fields):
                    self.test_data["job_id"] = result["id"]
                    self.log_result("/jobs/analyze", "PASS", f"Job analyzed: {result['id']}")
                    return True
                else:
                    self.log_result("/jobs/analyze", "FAIL", f"Missing fields: {set(required_fields) - set(result.keys())}")
            else:
                self.log_result("/jobs/analyze", "FAIL", f"Status: {response.status_code}, Body: {response.text[:200]}")
        except Exception as e:
            self.log_result("/jobs/analyze", "FAIL", f"Error: {e}")
        return False
    
    def test_optimize_sse(self):
        """Test /optimize SSE endpoint"""
        if "resume_id" not in self.test_data or "job_id" not in self.test_data:
            self.log_result("/optimize (SSE)", "SKIP", "Missing resume_id or job_id from previous tests")
            return False
        
        try:
            payload = {
                "resume_id": self.test_data["resume_id"],
                "job_id": self.test_data["job_id"]
            }
            
            response = requests.post(f"{BASE_URL}/optimize", json=payload, stream=True, timeout=TIMEOUT)
            
            if response.status_code == 200:
                if "text/event-stream" in response.headers.get("content-type", ""):
                    # Read first few SSE events
                    events_received = 0
                    for line in response.iter_lines(decode_unicode=True):
                        if line.startswith("data: "):
                            events_received += 1
                            if events_received >= 3:  # Check first 3 events
                                break
                    
                    if events_received > 0:
                        self.log_result("/optimize (SSE)", "PASS", f"SSE streaming working, received {events_received} events")
                        return True
                    else:
                        self.log_result("/optimize (SSE)", "FAIL", "No SSE events received")
                else:
                    self.log_result("/optimize (SSE)", "FAIL", f"Wrong content-type: {response.headers.get('content-type')}")
            else:
                self.log_result("/optimize (SSE)", "FAIL", f"Status: {response.status_code}, Body: {response.text[:200]}")
        except Exception as e:
            self.log_result("/optimize (SSE)", "FAIL", f"Error: {e}")
        return False
    
    def test_export_endpoints(self):
        """Test /export/{format} endpoints with template selection"""
        if "resume_id" not in self.test_data:
            self.log_result("/export/{format}", "SKIP", "Missing resume_id from previous tests")
            return False
        
        formats_tested = 0
        formats_passed = 0
        
        # Test templates endpoint first
        try:
            response = requests.get(f"{BASE_URL}/export/templates", timeout=10)
            if response.status_code == 200:
                templates = response.json()
                if isinstance(templates, list) and len(templates) > 0:
                    self.log_result("/export/templates", "PASS", f"Found {len(templates)} templates")
                else:
                    self.log_result("/export/templates", "FAIL", "No templates returned")
            else:
                self.log_result("/export/templates", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("/export/templates", "FAIL", f"Error: {e}")
        
        # Test PDF export with different templates
        for template in ["classic", "modern"]:
            formats_tested += 1
            try:
                payload = {
                    "resume_id": self.test_data["resume_id"],
                    "template": template
                }
                
                response = requests.post(f"{BASE_URL}/export/pdf", json=payload, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    if "html" in content_type or "pdf" in content_type:
                        formats_passed += 1
                        self.log_result(f"/export/pdf ({template})", "PASS", f"Content-Type: {content_type}")
                    else:
                        self.log_result(f"/export/pdf ({template})", "FAIL", f"Wrong content-type: {content_type}")
                else:
                    self.log_result(f"/export/pdf ({template})", "FAIL", f"Status: {response.status_code}")
            except Exception as e:
                self.log_result(f"/export/pdf ({template})", "FAIL", f"Error: {e}")
        
        # Test DOCX export
        formats_tested += 1
        try:
            payload = {
                "resume_id": self.test_data["resume_id"],
                "template": "classic"
            }
            
            response = requests.post(f"{BASE_URL}/export/docx", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                if "document" in content_type or "octet-stream" in content_type:
                    formats_passed += 1
                    self.log_result("/export/docx", "PASS", f"Content-Type: {content_type}")
                else:
                    self.log_result("/export/docx", "FAIL", f"Wrong content-type: {content_type}")
            else:
                self.log_result("/export/docx", "FAIL", f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("/export/docx", "FAIL", f"Error: {e}")
        
        return formats_passed == formats_tested
    
    def test_github_analyze(self):
        """Test /github/analyze endpoint"""
        try:
            payload = {"username": "octocat"}  # GitHub's mascot account
            
            response = requests.post(f"{BASE_URL}/github/analyze", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                result = response.json()
                required_fields = ["username", "profile_url", "impact_metrics", "tech_stack", "top_repositories", "project_highlights", "resume_bullet_points"]
                if all(field in result for field in required_fields):
                    self.log_result("/github/analyze", "PASS", f"GitHub analysis for {result['username']}")
                    return True
                else:
                    self.log_result("/github/analyze", "FAIL", f"Missing fields: {set(required_fields) - set(result.keys())}")
            else:
                self.log_result("/github/analyze", "FAIL", f"Status: {response.status_code}, Body: {response.text[:200]}")
        except Exception as e:
            self.log_result("/github/analyze", "FAIL", f"Error: {e}")
        return False
    
    def test_error_handling(self):
        """Test error handling across endpoints"""
        error_tests = [
            # Invalid file type
            ("/resume/upload", "POST", {"files": {"file": ("test.exe", b"invalid", "application/exe")}}),
            # Missing required fields
            ("/jobs/analyze", "POST", {"json": {}}),
            # Invalid resume ID
            ("/optimize", "POST", {"json": {"resume_id": "invalid", "job_id": "invalid"}}),
            # Invalid export format
            ("/export/invalid", "POST", {"json": {"resume_id": "test"}}),
            # Invalid GitHub username
            ("/github/analyze", "POST", {"json": {"username": ""}}),
        ]
        
        passed = 0
        total = len(error_tests)
        
        for endpoint, method, kwargs in error_tests:
            try:
                if method == "POST":
                    response = requests.post(f"{BASE_URL}{endpoint}", timeout=10, **kwargs)
                else:
                    response = requests.get(f"{BASE_URL}{endpoint}", timeout=10, **kwargs)
                
                if 400 <= response.status_code < 500:
                    passed += 1
                    self.log_result(f"Error handling {endpoint}", "PASS", f"Status: {response.status_code}")
                else:
                    self.log_result(f"Error handling {endpoint}", "FAIL", f"Expected 4xx, got: {response.status_code}")
            except Exception as e:
                self.log_result(f"Error handling {endpoint}", "FAIL", f"Error: {e}")
        
        return passed == total
    
    def run_all_tests(self):
        """Run all API validation tests"""
        print("🚀 Starting Backend API Validation")
        print("=" * 50)
        
        # Test basic connectivity
        if not self.test_health_endpoint():
            print("❌ Backend not accessible, stopping tests")
            return
        
        # Test core endpoints in order
        self.test_resume_upload()
        self.test_jobs_analyze()
        self.test_optimize_sse()
        self.test_export_endpoints()
        self.test_github_analyze()
        self.test_error_handling()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 VALIDATION SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for r in self.results.values() if r["status"] == "PASS")
        failed = sum(1 for r in self.results.values() if r["status"] == "FAIL")
        skipped = sum(1 for r in self.results.values() if r["status"] == "SKIP")
        
        print(f"✅ PASSED: {passed}")
        print(f"❌ FAILED: {failed}")
        print(f"⏭️  SKIPPED: {skipped}")
        print(f"📈 SUCCESS RATE: {passed/(passed+failed)*100:.1f}%" if (passed+failed) > 0 else "N/A")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for endpoint, result in self.results.items():
                if result["status"] == "FAIL":
                    print(f"   {endpoint}: {result['details']}")

if __name__ == "__main__":
    validator = APIValidator()
    validator.run_all_tests()
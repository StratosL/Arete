#!/usr/bin/env python3
"""
Comprehensive System Validation for Arete Application
Tests all MVP features end-to-end
"""

import asyncio
import json
import os
import requests
import tempfile
from pathlib import Path
from typing import Dict, List, Any
import time

class SystemValidator:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.results = {}
        self.test_data = {}
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test result"""
        self.results[test_name] = {
            "status": status,
            "details": details,
            "timestamp": time.time()
        }
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   {details}")

    def test_backend_health(self) -> bool:
        """Test if backend is running"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                self.log_test("Backend Health", "PASS", "FastAPI docs accessible")
                return True
            else:
                self.log_test("Backend Health", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Health", "FAIL", f"Connection error: {str(e)}")
            return False

    def create_test_resume(self) -> str:
        """Create test resume file"""
        resume_content = """John Doe
Software Engineer
john.doe@email.com | +1-555-0123 | San Francisco, CA
GitHub: https://github.com/johndoe | LinkedIn: linkedin.com/in/johndoe

EXPERIENCE
Senior Software Engineer | TechCorp | 2020-2023
• Built scalable web applications using Python and React
• Led team of 5 developers on microservices architecture
• Implemented CI/CD pipelines reducing deployment time by 60%
• Technologies: Python, FastAPI, React, PostgreSQL, Docker, AWS

Software Engineer | StartupXYZ | 2018-2020
• Developed REST APIs serving 100K+ daily requests
• Optimized database queries improving performance by 40%
• Technologies: Python, Django, MySQL, Redis

SKILLS
Programming Languages: Python, JavaScript, TypeScript, SQL
Frameworks: FastAPI, Django, React, Vue.js
Tools: Docker, Kubernetes, Git, Jenkins, AWS
Databases: PostgreSQL, MySQL, Redis, MongoDB

PROJECTS
E-commerce Platform | 2023
• Full-stack application with 10K+ users
• Microservices architecture with Docker containers
• Technologies: Python, FastAPI, React, PostgreSQL
• GitHub: github.com/johndoe/ecommerce

Task Management App | 2022
• Real-time collaboration features using WebSockets
• Technologies: Python, Django, React, Redis
• 500+ GitHub stars

EDUCATION
Bachelor of Science in Computer Science | Stanford University | 2018
GPA: 3.8/4.0
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(resume_content)
            return f.name

    def test_resume_upload(self) -> bool:
        """Test resume upload and parsing"""
        try:
            resume_file = self.create_test_resume()
            
            with open(resume_file, 'rb') as f:
                files = {'file': ('test_resume.txt', f, 'text/plain')}
                data = {'github_url': 'https://github.com/johndoe'}
                
                response = requests.post(
                    f"{self.base_url}/resume/upload",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            os.unlink(resume_file)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success' and result.get('data'):
                    self.test_data['resume_id'] = result['data']['id']
                    self.test_data['resume_data'] = result['data']
                    self.log_test("Resume Upload", "PASS", f"Resume ID: {result['data']['id']}")
                    return True
                else:
                    self.log_test("Resume Upload", "FAIL", "Invalid response structure")
                    return False
            else:
                self.log_test("Resume Upload", "FAIL", f"Status: {response.status_code}, {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Resume Upload", "FAIL", f"Error: {str(e)}")
            return False

    def test_resume_parsing_quality(self) -> bool:
        """Test quality of resume parsing"""
        if 'resume_data' not in self.test_data:
            self.log_test("Resume Parsing Quality", "SKIP", "No resume data available")
            return False
            
        try:
            data = self.test_data['resume_data']
            issues = []
            
            # Check personal info
            personal = data.get('personal_info', {})
            if not personal.get('name'):
                issues.append("Missing name")
            if not personal.get('email'):
                issues.append("Missing email")
                
            # Check experience
            experience = data.get('experience', [])
            if not experience:
                issues.append("No experience found")
            elif len(experience) < 2:
                issues.append("Expected 2+ experience entries")
                
            # Check skills
            skills = data.get('skills', {})
            if not skills.get('technical'):
                issues.append("No technical skills found")
                
            # Check projects
            projects = data.get('projects', [])
            if not projects:
                issues.append("No projects found")
                
            if issues:
                self.log_test("Resume Parsing Quality", "FAIL", f"Issues: {', '.join(issues)}")
                return False
            else:
                self.log_test("Resume Parsing Quality", "PASS", "All sections parsed correctly")
                return True
                
        except Exception as e:
            self.log_test("Resume Parsing Quality", "FAIL", f"Error: {str(e)}")
            return False

    def test_github_integration(self) -> bool:
        """Test GitHub profile analysis"""
        try:
            response = requests.post(
                f"{self.base_url}/github/analyze",
                json={"username": "octocat"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                required_fields = ['username', 'impact_metrics', 'tech_stack', 'resume_bullet_points']
                missing = [field for field in required_fields if field not in result]
                
                if missing:
                    self.log_test("GitHub Integration", "FAIL", f"Missing fields: {missing}")
                    return False
                else:
                    self.log_test("GitHub Integration", "PASS", f"Analyzed {result['username']}")
                    return True
            else:
                self.log_test("GitHub Integration", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("GitHub Integration", "FAIL", f"Error: {str(e)}")
            return False

    def test_job_analysis_text(self) -> bool:
        """Test job analysis with text input"""
        try:
            job_text = """
            Senior Python Developer - Remote
            
            We are looking for a Senior Python Developer to join our team.
            
            Requirements:
            - 5+ years of Python development experience
            - Experience with FastAPI or Django
            - Knowledge of PostgreSQL and Redis
            - Docker and Kubernetes experience
            - AWS cloud platform experience
            
            Preferred:
            - React or Vue.js frontend experience
            - CI/CD pipeline experience
            - Microservices architecture
            
            Responsibilities:
            - Design and develop scalable web applications
            - Lead technical architecture decisions
            - Mentor junior developers
            - Collaborate with product team
            """
            
            response = requests.post(
                f"{self.base_url}/jobs/analyze",
                json={"job_text": job_text},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.test_data['job_id'] = result['id']
                self.test_data['job_analysis'] = result
                
                required_fields = ['title', 'required_skills', 'technologies', 'experience_level']
                missing = [field for field in required_fields if field not in result]
                
                if missing:
                    self.log_test("Job Analysis (Text)", "FAIL", f"Missing fields: {missing}")
                    return False
                else:
                    self.log_test("Job Analysis (Text)", "PASS", f"Job: {result['title']}")
                    return True
            else:
                self.log_test("Job Analysis (Text)", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Job Analysis (Text)", "FAIL", f"Error: {str(e)}")
            return False

    def test_job_analysis_url(self) -> bool:
        """Test job analysis with URL scraping"""
        try:
            # Use a reliable test URL (GitHub careers page)
            response = requests.post(
                f"{self.base_url}/jobs/analyze",
                json={"job_url": "https://github.com/about/careers"},
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_test("Job Analysis (URL)", "PASS", f"Scraped and analyzed URL")
                return True
            else:
                self.log_test("Job Analysis (URL)", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Job Analysis (URL)", "FAIL", f"Error: {str(e)}")
            return False

    def test_optimization_streaming(self) -> bool:
        """Test AI optimization with SSE streaming"""
        if 'resume_id' not in self.test_data or 'job_id' not in self.test_data:
            self.log_test("AI Optimization", "SKIP", "Missing resume or job data")
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/optimize",
                json={
                    "resume_id": self.test_data['resume_id'],
                    "job_id": self.test_data['job_id']
                },
                stream=True,
                timeout=60
            )
            
            if response.status_code == 200:
                suggestions_found = False
                completed = False
                
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            try:
                                data = json.loads(line_str[6:])
                                if data.get('suggestions'):
                                    suggestions_found = True
                                if data.get('completed'):
                                    completed = True
                                    break
                            except json.JSONDecodeError:
                                continue
                
                if completed and suggestions_found:
                    self.log_test("AI Optimization", "PASS", "Streaming completed with suggestions")
                    return True
                else:
                    self.log_test("AI Optimization", "FAIL", "Incomplete optimization")
                    return False
            else:
                self.log_test("AI Optimization", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("AI Optimization", "FAIL", f"Error: {str(e)}")
            return False

    def test_cover_letter_generation(self) -> bool:
        """Test cover letter generation"""
        if 'resume_id' not in self.test_data or 'job_id' not in self.test_data:
            self.log_test("Cover Letter Generation", "SKIP", "Missing resume or job data")
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/optimize/cover-letter",
                json={
                    "resume_id": self.test_data['resume_id'],
                    "job_id": self.test_data['job_id']
                },
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('cover_letter') and len(result['cover_letter']) > 100:
                    self.log_test("Cover Letter Generation", "PASS", f"Generated {len(result['cover_letter'])} chars")
                    return True
                else:
                    self.log_test("Cover Letter Generation", "FAIL", "Cover letter too short or missing")
                    return False
            else:
                self.log_test("Cover Letter Generation", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Cover Letter Generation", "FAIL", f"Error: {str(e)}")
            return False

    def test_document_export_pdf(self) -> bool:
        """Test PDF export"""
        if 'resume_id' not in self.test_data:
            self.log_test("PDF Export", "SKIP", "Missing resume data")
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/export/pdf",
                json={"resume_id": self.test_data['resume_id']},
                timeout=30
            )
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'html' in content_type or 'pdf' in content_type:
                    self.log_test("PDF Export", "PASS", f"Content-Type: {content_type}")
                    return True
                else:
                    self.log_test("PDF Export", "FAIL", f"Unexpected content-type: {content_type}")
                    return False
            else:
                self.log_test("PDF Export", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("PDF Export", "FAIL", f"Error: {str(e)}")
            return False

    def test_document_export_docx(self) -> bool:
        """Test DOCX export"""
        if 'resume_id' not in self.test_data:
            self.log_test("DOCX Export", "SKIP", "Missing resume data")
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/export/docx",
                json={"resume_id": self.test_data['resume_id']},
                timeout=30
            )
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'officedocument' in content_type or 'octet-stream' in content_type:
                    self.log_test("DOCX Export", "PASS", f"Content-Type: {content_type}")
                    return True
                else:
                    self.log_test("DOCX Export", "FAIL", f"Unexpected content-type: {content_type}")
                    return False
            else:
                self.log_test("DOCX Export", "FAIL", f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("DOCX Export", "FAIL", f"Error: {str(e)}")
            return False

    def run_validation(self):
        """Run complete system validation"""
        print("🚀 Starting Arete System Validation")
        print("=" * 50)
        
        # Core infrastructure tests
        if not self.test_backend_health():
            print("\n❌ Backend not accessible - stopping validation")
            return self.generate_report()
        
        # MVP Feature Tests
        tests = [
            ("Resume Upload & Parsing", self.test_resume_upload),
            ("Resume Parsing Quality", self.test_resume_parsing_quality),
            ("GitHub Integration", self.test_github_integration),
            ("Job Analysis (Text)", self.test_job_analysis_text),
            ("Job Analysis (URL)", self.test_job_analysis_url),
            ("AI Optimization", self.test_optimization_streaming),
            ("Cover Letter Generation", self.test_cover_letter_generation),
            ("PDF Export", self.test_document_export_pdf),
            ("DOCX Export", self.test_document_export_docx),
        ]
        
        print("\n📋 Running MVP Feature Tests")
        print("-" * 30)
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log_test(test_name, "ERROR", f"Unexpected error: {str(e)}")
        
        return self.generate_report()

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        total_tests = len(self.results)
        passed = sum(1 for r in self.results.values() if r['status'] == 'PASS')
        failed = sum(1 for r in self.results.values() if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.results.values() if r['status'] == 'SKIP')
        errors = sum(1 for r in self.results.values() if r['status'] == 'ERROR')
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "errors": errors,
                "success_rate": f"{(passed/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            "results": self.results,
            "test_data": {k: v for k, v in self.test_data.items() if k != 'resume_data'}
        }
        
        print("\n" + "=" * 50)
        print("📊 VALIDATION REPORT")
        print("=" * 50)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Skipped: {skipped}")
        print(f"🔥 Errors: {errors}")
        print(f"Success Rate: {report['summary']['success_rate']}")
        
        # Critical failures
        critical_tests = [
            "Backend Health",
            "Resume Upload",
            "Job Analysis (Text)",
            "AI Optimization"
        ]
        
        critical_failures = [
            test for test in critical_tests 
            if self.results.get(test, {}).get('status') in ['FAIL', 'ERROR']
        ]
        
        if critical_failures:
            print(f"\n🚨 CRITICAL FAILURES: {', '.join(critical_failures)}")
            print("System is not ready for production")
        else:
            print(f"\n✅ All critical features operational")
            if failed == 0 and errors == 0:
                print("🎉 System validation PASSED - Ready for demo!")
            else:
                print("⚠️  Some non-critical issues found")
        
        return report

if __name__ == "__main__":
    validator = SystemValidator()
    report = validator.run_validation()
    
    # Save report
    with open("validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: validation_report.json")
#!/usr/bin/env python3
"""
Frontend Integration Validation
Tests frontend-backend integration and UI components
"""

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class FrontendValidator:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"
        self.results = {}
        
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

    def test_frontend_accessibility(self) -> bool:
        """Test if frontend is running"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Accessibility", "PASS", "React app accessible")
                return True
            else:
                self.log_test("Frontend Accessibility", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Accessibility", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_api_integration(self) -> bool:
        """Test frontend-backend API integration"""
        try:
            # Test CORS and API connectivity
            response = requests.options(f"{self.backend_url}/resume/upload")
            cors_headers = response.headers.get('Access-Control-Allow-Origin', '')
            
            if '*' in cors_headers or 'localhost:3000' in cors_headers:
                self.log_test("API Integration", "PASS", "CORS configured correctly")
                return True
            else:
                self.log_test("API Integration", "WARN", f"CORS headers: {cors_headers}")
                return True  # Not critical for MVP
        except Exception as e:
            self.log_test("API Integration", "FAIL", f"Error: {str(e)}")
            return False

    def test_component_rendering(self) -> bool:
        """Test if key components render without errors"""
        try:
            # Setup headless Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.frontend_url)
            
            # Wait for React to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check for key components
            components_found = []
            
            # Look for upload component
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Upload') or contains(text(), 'resume')]"):
                components_found.append("Upload Component")
            
            # Look for main app structure
            if driver.find_elements(By.TAG_NAME, "main") or driver.find_elements(By.CLASS_NAME, "App"):
                components_found.append("Main App")
            
            driver.quit()
            
            if components_found:
                self.log_test("Component Rendering", "PASS", f"Found: {', '.join(components_found)}")
                return True
            else:
                self.log_test("Component Rendering", "FAIL", "No key components found")
                return False
                
        except Exception as e:
            self.log_test("Component Rendering", "FAIL", f"Error: {str(e)}")
            return False

    def run_frontend_validation(self):
        """Run frontend validation tests"""
        print("\n🎨 Frontend Integration Validation")
        print("=" * 40)
        
        tests = [
            ("Frontend Accessibility", self.test_frontend_accessibility),
            ("API Integration", self.test_api_integration),
            ("Component Rendering", self.test_component_rendering),
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log_test(test_name, "ERROR", f"Unexpected error: {str(e)}")
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r['status'] == 'PASS')
        
        print(f"\n📊 Frontend Tests: {passed}/{total} passed")
        return self.results

if __name__ == "__main__":
    validator = FrontendValidator()
    results = validator.run_frontend_validation()
    
    with open("frontend_validation.json", "w") as f:
        json.dump(results, f, indent=2)
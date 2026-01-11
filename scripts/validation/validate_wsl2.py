#!/usr/bin/env python3
"""
WSL2 Environment Validation Script for Arete
Checks WSL2-specific requirements and Docker integration.
"""

import os
import sys
import subprocess
import platform

def check_wsl2_environment():
    """Check if running in WSL2"""
    try:
        # Check if we're in WSL
        with open('/proc/version', 'r') as f:
            version_info = f.read().lower()
            if 'microsoft' in version_info or 'wsl' in version_info:
                print("✅ Running in WSL environment")
                return True
            else:
                print("ℹ️  Not running in WSL (native Linux)")
                return True
    except FileNotFoundError:
        print("ℹ️  Not running in Linux environment")
        return False

def check_python_commands():
    """Check available Python commands"""
    commands = ['python3', 'python']
    available = []
    
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            available.append((cmd, version))
            print(f"✅ {cmd}: {version}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {cmd}: Not available")
    
    if not available:
        print("❌ No Python installation found")
        return False
    
    return True

def check_docker_wsl2_integration():
    """Check Docker Desktop WSL2 integration"""
    try:
        # Test Docker daemon connection
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, check=True)
        
        # Check if Docker is using WSL2 backend
        if 'wsl' in result.stdout.lower():
            print("✅ Docker WSL2 integration active")
        else:
            print("✅ Docker daemon accessible")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker daemon not accessible: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ Docker command not found")
        return False

def check_file_permissions():
    """Check file permissions in WSL2 mounted directories"""
    current_dir = os.getcwd()
    
    # Check if we're in a Windows mount point
    if current_dir.startswith('/mnt/'):
        print(f"ℹ️  Working in Windows mount: {current_dir}")
        
        # Test file creation
        test_file = '.wsl2_test'
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print("✅ File operations work correctly")
            return True
        except Exception as e:
            print(f"❌ File permission issue: {e}")
            return False
    else:
        print(f"✅ Working in native Linux filesystem: {current_dir}")
        return True

def main():
    """Main validation function"""
    print("🔍 Validating WSL2 environment for Arete...")
    print()
    
    checks = [
        ("WSL2 Environment", check_wsl2_environment),
        ("Python Commands", check_python_commands),
        ("Docker Integration", check_docker_wsl2_integration),
        ("File Permissions", check_file_permissions)
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"📋 Checking {name}...")
        if not check_func():
            all_passed = False
        print()
    
    if all_passed:
        print("✅ WSL2 environment validation completed successfully!")
        print("   Your environment is ready for Arete development.")
    else:
        print("❌ Some validation checks failed.")
        print("   Please address the issues above before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Environment validation script for Arete
Checks that all required environment variables and services are configured correctly.
"""

import os
import sys
from typing import List, Tuple

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: python-dotenv not installed")
    print("   Run: pip install python-dotenv")
    sys.exit(1)

def check_env_vars() -> List[str]:
    """Check required environment variables"""
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_KEY", 
        "SUPABASE_SERVICE_KEY",
        "CLAUDE_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return missing_vars

def check_supabase_connection() -> Tuple[bool, str]:
    """Test Supabase connection"""
    try:
        from supabase import create_client
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            return False, "Missing Supabase credentials"
        
        # Just try to create the client - if credentials are valid, this will work
        supabase = create_client(url, key)
        return True, "Client created successfully"
        
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def check_claude_api() -> Tuple[bool, str]:
    """Test Claude API connection"""
    try:
        import litellm
        
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            return False, "Missing Claude API key"
        
        # Set the API key
        os.environ["ANTHROPIC_API_KEY"] = api_key
        
        # Simple test request
        response = litellm.completion(
            model="claude-sonnet-4-5",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return True, "API key valid"
        
    except Exception as e:
        return False, f"API test failed: {str(e)}"

def main():
    """Main validation function"""
    print("🔍 Validating Arete environment...")
    
    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded .env file")
    except ImportError:
        print("❌ Error: python-dotenv not installed")
        sys.exit(1)
    
    # Check environment variables
    print("\n📋 Checking environment variables...")
    missing_vars = check_env_vars()
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please check your .env file")
        sys.exit(1)
    else:
        print("✅ All required environment variables are set")
    
    # Check Supabase connection
    print("\n🗄️  Testing Supabase connection...")
    supabase_ok, supabase_msg = check_supabase_connection()
    
    if supabase_ok:
        print(f"✅ Supabase: {supabase_msg}")
    else:
        print(f"❌ Supabase: {supabase_msg}")
        sys.exit(1)
    
    # Check Claude API
    print("\n🤖 Testing Claude API...")
    claude_ok, claude_msg = check_claude_api()
    
    if claude_ok:
        print(f"✅ Claude API: {claude_msg}")
    else:
        print(f"❌ Claude API: {claude_msg}")
        sys.exit(1)
    
    print("\n✅ Environment validation completed successfully!")
    print("   Your Arete setup is ready to use.")

if __name__ == "__main__":
    main()

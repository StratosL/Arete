#!/usr/bin/env python3
"""
Supabase Setup Script for Arete
Creates storage buckets and policies that can't be handled by migrations.
"""

import os
import sys
from typing import Optional

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions


def get_supabase_client() -> Client:
    """Create Supabase client with service key for admin operations"""
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        print("   Check your .env file or environment variables")
        sys.exit(1)
    
    return create_client(url, service_key)


def create_storage_bucket(supabase: Client, bucket_name: str) -> bool:
    """Create storage bucket if it doesn't exist"""
    try:
        # Check if bucket exists
        buckets = supabase.storage.list_buckets()
        existing_buckets = [bucket.name for bucket in buckets]
        
        if bucket_name in existing_buckets:
            print(f"✅ Bucket '{bucket_name}' already exists")
            return True
        
        # Create bucket
        supabase.storage.create_bucket(bucket_name, options={"public": False})
        print(f"✅ Created bucket '{bucket_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create bucket '{bucket_name}': {str(e)}")
        return False


def create_storage_policies(supabase: Client, bucket_name: str) -> bool:
    """Create storage policies for the bucket"""
    policies = [
        {
            "name": f"{bucket_name}_select_policy",
            "definition": f"""
                CREATE POLICY "{bucket_name}_select_policy" ON storage.objects
                FOR SELECT USING (
                    bucket_id = '{bucket_name}' AND 
                    auth.uid()::text = (storage.foldername(name))[1]
                );
            """
        },
        {
            "name": f"{bucket_name}_insert_policy", 
            "definition": f"""
                CREATE POLICY "{bucket_name}_insert_policy" ON storage.objects
                FOR INSERT WITH CHECK (
                    bucket_id = '{bucket_name}' AND 
                    auth.uid()::text = (storage.foldername(name))[1]
                );
            """
        },
        {
            "name": f"{bucket_name}_update_policy",
            "definition": f"""
                CREATE POLICY "{bucket_name}_update_policy" ON storage.objects
                FOR UPDATE USING (
                    bucket_id = '{bucket_name}' AND 
                    auth.uid()::text = (storage.foldername(name))[1]
                );
            """
        },
        {
            "name": f"{bucket_name}_delete_policy",
            "definition": f"""
                CREATE POLICY "{bucket_name}_delete_policy" ON storage.objects
                FOR DELETE USING (
                    bucket_id = '{bucket_name}' AND 
                    auth.uid()::text = (storage.foldername(name))[1]
                );
            """
        }
    ]
    
    try:
        for policy in policies:
            # Drop policy if exists (idempotent)
            supabase.rpc("exec_sql", {
                "sql": f"DROP POLICY IF EXISTS \"{policy['name']}\" ON storage.objects;"
            })
            
            # Create policy
            supabase.rpc("exec_sql", {"sql": policy["definition"]})
            
        print(f"✅ Created storage policies for '{bucket_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create storage policies: {str(e)}")
        return False


def run_migrations(supabase: Client) -> bool:
    """Run database migrations"""
    migrations_dir = "supabase/migrations"
    
    if not os.path.exists(migrations_dir):
        print(f"⚠️  No migrations directory found at {migrations_dir}")
        return True
    
    try:
        migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
        
        for migration_file in migration_files:
            migration_path = os.path.join(migrations_dir, migration_file)
            
            with open(migration_path, 'r') as f:
                sql_content = f.read()
            
            # Execute migration
            supabase.rpc("exec_sql", {"sql": sql_content})
            print(f"✅ Applied migration: {migration_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to run migrations: {str(e)}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Supabase for Arete...")
    
    # Create Supabase client
    supabase = get_supabase_client()
    
    # Run migrations
    print("\n📊 Running database migrations...")
    if not run_migrations(supabase):
        sys.exit(1)
    
    # Create storage bucket
    print("\n🗄️  Setting up storage...")
    if not create_storage_bucket(supabase, "resumes"):
        sys.exit(1)
    
    # Create storage policies
    print("\n🔒 Setting up storage policies...")
    if not create_storage_policies(supabase, "resumes"):
        sys.exit(1)
    
    print("\n✅ Supabase setup completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Start the application: docker-compose up")
    print("   2. Upload a resume to test the setup")


if __name__ == "__main__":
    main()

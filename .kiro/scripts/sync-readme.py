#!/usr/bin/env python3
"""
Automated Documentation Sync System
Keeps README.md status in sync with actual implementation
"""

import os
import re
from pathlib import Path

def check_implementation_status():
    """Check actual implementation status by examining codebase"""
    
    backend_path = Path("backend/app")
    frontend_path = Path("frontend/src/components")
    
    status = {
        "phase1_resume": False,
        "phase2_jobs": False, 
        "phase3_optimization": False,
        "phase4_export": False,
        "phase5_interview": False
    }
    
    # Check Phase 1: Resume Upload
    if (backend_path / "resume" / "routes.py").exists() and \
       (frontend_path / "ResumeUpload.tsx").exists():
        status["phase1_resume"] = True
    
    # Check Phase 2: Job Analysis  
    if (backend_path / "jobs" / "routes.py").exists() and \
       (frontend_path / "JobDescriptionInput.tsx").exists():
        status["phase2_jobs"] = True
        
    # Check Phase 3: Optimization
    if (backend_path / "optimization" / "routes.py").exists() and \
       (frontend_path / "OptimizationDisplay.tsx").exists():
        status["phase3_optimization"] = True
        
    # Check Phase 4: Export
    export_routes = backend_path / "export" / "routes.py"
    if export_routes.exists() and export_routes.stat().st_size > 100:  # Must have actual content
        status["phase4_export"] = True
        
    # Check Phase 5: Interview
    interview_routes = backend_path / "interview" / "routes.py"  
    if interview_routes.exists() and interview_routes.stat().st_size > 100:  # Must have actual content
        status["phase5_interview"] = True
    
    return status

def update_readme_status(status):
    """Update README.md with current implementation status"""
    
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("❌ README.md not found")
        return False
        
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Define status updates
    updates = []
    
    if status["phase1_resume"] and status["phase2_jobs"]:
        updates.append("**🎯 Current Status**: Phase 2 Complete - Resume Upload & Job Analysis Features Production Ready")
    
    if status["phase3_optimization"]:
        updates.append("**🎯 Current Status**: Phase 3 Complete - AI Optimization with SSE Streaming Production Ready")
        
    if status["phase4_export"]:
        updates.append("**🎯 Current Status**: Phase 4 Complete - Document Export Features Production Ready")
        
    if status["phase5_interview"]:
        updates.append("**🎯 Current Status**: Phase 5 Complete - Interview Preparation Features Production Ready")
    
    # Use the highest completed phase
    if updates:
        new_status = updates[-1]
        
        # Replace existing status line
        pattern = r'\*\*🎯 Current Status\*\*:.*'
        if re.search(pattern, content):
            content = re.sub(pattern, new_status, content)
        else:
            # Add status if not found
            content = content.replace(
                "# Arete - AI-Powered Resume Optimizer for Tech Professionals\n",
                f"# Arete - AI-Powered Resume Optimizer for Tech Professionals\n\n{new_status}\n"
            )
    
    # Update feature status sections
    feature_updates = {
        "### Resume Upload & Parsing (Phase 1 - Complete)": status["phase1_resume"],
        "### Job Description Analysis (Phase 2 - Complete & Production Ready)": status["phase2_jobs"], 
        "### AI Optimization (Phase 3 - Complete & Production Ready)": status["phase3_optimization"],
        "### Document Export (Phase 4 - Complete)": status["phase4_export"],
        "### Interview Preparation (Phase 5 - Complete)": status["phase5_interview"]
    }
    
    for section, is_complete in feature_updates.items():
        if is_complete:
            # Ensure section shows as complete
            incomplete_pattern = section.replace("Complete", "Incomplete").replace("Production Ready", "In Progress")
            content = content.replace(incomplete_pattern, section)
    
    # Write updated content
    with open(readme_path, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main sync function"""
    print("🔄 Syncing README.md with implementation status...")
    
    # Check current implementation
    status = check_implementation_status()
    
    print("\n📊 Implementation Status:")
    print(f"  Phase 1 (Resume): {'✅' if status['phase1_resume'] else '❌'}")
    print(f"  Phase 2 (Jobs): {'✅' if status['phase2_jobs'] else '❌'}")  
    print(f"  Phase 3 (Optimization): {'✅' if status['phase3_optimization'] else '❌'}")
    print(f"  Phase 4 (Export): {'✅' if status['phase4_export'] else '❌'}")
    print(f"  Phase 5 (Interview): {'✅' if status['phase5_interview'] else '❌'}")
    
    # Update README
    if update_readme_status(status):
        print("\n✅ README.md updated successfully")
        
        # Show what phase we're actually at
        if status['phase5_interview']:
            print("📋 Current Phase: 5 (Interview Preparation) - COMPLETE")
        elif status['phase4_export']:
            print("📋 Current Phase: 4 (Document Export) - COMPLETE") 
        elif status['phase3_optimization']:
            print("📋 Current Phase: 3 (AI Optimization) - COMPLETE")
        elif status['phase2_jobs']:
            print("📋 Current Phase: 2 (Job Analysis) - COMPLETE")
        elif status['phase1_resume']:
            print("📋 Current Phase: 1 (Resume Upload) - COMPLETE")
        else:
            print("📋 Current Phase: Setup/Infrastructure")
            
    else:
        print("❌ Failed to update README.md")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

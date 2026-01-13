import asyncio
import json
from typing import AsyncGenerator

from fastapi import HTTPException

from app.core.database import get_supabase_service_client
from app.core.llm import stream_llm_response
from app.optimization.schemas import OptimizationProgress, OptimizationSuggestion


class OptimizationService:
    """Service for AI-powered resume optimization"""

    async def get_resume_job_data(self, resume_id: str, job_id: str) -> tuple[dict, dict]:
        """Fetch and validate resume and job data"""
        supabase = get_supabase_service_client()
        
        # Fetch resume data
        resume_response = (
            supabase.table("resumes")
            .select("*")
            .eq("id", resume_id)
            .execute()
        )
        if not resume_response.data:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        resume_record = resume_response.data[0]
        resume_data = resume_record.get("parsed_data", {})
        
        # Fetch job analysis data
        job_response = supabase.table("jobs").select("*").eq("id", job_id).execute()
        if not job_response.data:
            raise HTTPException(status_code=404, detail="Job analysis not found")
        
        job_record = job_response.data[0]
        job_analysis = job_record.get("analysis", {})
        
        return resume_data, job_analysis

    async def save_optimization(self, resume_id: str, optimized_data: dict) -> None:
        """Save optimization results to database"""
        supabase = get_supabase_service_client()
        
        supabase.table("resumes").update({
            "optimized_data": optimized_data
        }).eq("id", resume_id).execute()

    async def optimize_resume(
        self, resume_data: dict, job_analysis: dict
    ) -> AsyncGenerator[OptimizationProgress, None]:
        """Stream optimization suggestions for resume based on job requirements"""
        
        # Step 1: Analyze alignment
        yield OptimizationProgress(
            step="analyzing",
            progress=10,
            message="Analyzing resume-job alignment...",
            suggestions=[],
            completed=False
        )
        await asyncio.sleep(1)

        # Step 2: Generate keyword suggestions
        yield OptimizationProgress(
            step="keywords",
            progress=30,
            message="Identifying missing keywords...",
            suggestions=[],
            completed=False
        )
        await asyncio.sleep(2)

        keyword_suggestions = await self._generate_keyword_suggestions(resume_data, job_analysis)
        
        yield OptimizationProgress(
            step="keywords",
            progress=50,
            message="Generated keyword suggestions",
            suggestions=keyword_suggestions,
            completed=False
        )
        await asyncio.sleep(1)

        # Step 3: Enhance experience descriptions
        yield OptimizationProgress(
            step="experience",
            progress=70,
            message="Enhancing experience descriptions...",
            suggestions=keyword_suggestions,
            completed=False
        )
        await asyncio.sleep(2)

        experience_suggestions = await self._enhance_experience(resume_data, job_analysis)
        all_suggestions = keyword_suggestions + experience_suggestions

        yield OptimizationProgress(
            step="experience",
            progress=90,
            message="Enhanced experience descriptions",
            suggestions=all_suggestions,
            completed=False
        )
        await asyncio.sleep(1)

        # Step 4: Final optimization
        suggestion_count = len(all_suggestions)
        completion_msg = f"Optimization complete! Generated {suggestion_count} suggestions."
        yield OptimizationProgress(
            step="complete",
            progress=100,
            message=completion_msg,
            suggestions=all_suggestions,
            completed=True
        )

    async def generate_cover_letter(self, resume_data: dict, job_analysis: dict) -> str:
        """Generate tailored cover letter based on resume and job analysis"""
        
        personal_info = resume_data.get('personal_info', {})
        experience = resume_data.get('experience', [])
        skills = resume_data.get('skills', {})
        
        prompt = f"""
        Write a professional cover letter for a tech professional applying to this job.
        
        CANDIDATE INFO:
        Name: {personal_info.get('name', 'Candidate')}
        Current Role: {experience[0].get('title', 'Software Engineer') if experience else 'Software Engineer'}
        Key Skills: {', '.join(skills.get('technical', [])[:5])}
        
        JOB INFO:
        Title: {job_analysis.get('title', 'Software Engineer')}
        Company: {job_analysis.get('company', 'Company')}
        Required Skills: {', '.join(job_analysis.get('required_skills', [])[:5])}
        Technologies: {', '.join(job_analysis.get('technologies', [])[:3])}
        
        REQUIREMENTS:
        - Professional tone, 3-4 paragraphs
        - Mention specific technologies from job requirements
        - Highlight relevant experience alignment
        - Show enthusiasm for the role and company
        - End with call to action
        - No placeholder text like [Company Name]
        
        Return ONLY the cover letter text, no additional formatting or explanations.
        """

        messages = [{"role": "user", "content": prompt}]
        response_text = ""
        
        async for chunk in stream_llm_response(messages):
            response_text += chunk

        return response_text.strip()

    async def _generate_keyword_suggestions(
        self, resume_data: dict, job_analysis: dict
    ) -> list[OptimizationSuggestion]:
        """Generate keyword optimization suggestions"""
        
        # Extract and normalize existing skills
        existing_skills = self._get_existing_skills(resume_data)
        
        # Filter job requirements to exclude existing skills
        missing_skills = self._find_missing_skills(job_analysis, existing_skills)
        
        if not missing_skills:
            return []
        
        prompt = f"""
        Analyze this resume against job requirements and suggest ONLY missing keywords.
        
        Job Requirements (missing from resume):
        - Required Skills: {', '.join(missing_skills.get('required_skills', []))}
        - Technologies: {', '.join(missing_skills.get('technologies', []))}
        
        IMPORTANT: Only suggest skills that are NOT already in the resume.
        
        Return ONLY a JSON array of suggestions in this format:
        [
            {{
                "section": "skills",
                "type": "add_keyword",
                "original": "Current skill list",
                "suggested": "Enhanced skill list with missing keywords",
                "reason": "Job requires X but resume doesn't mention it",
                "impact": "high"
            }}
        ]
        """

        messages = [{"role": "user", "content": prompt}]
        response_text = ""
        
        async for chunk in stream_llm_response(messages):
            response_text += chunk

        try:
            json_str = response_text.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:-3]
            elif json_str.startswith('```'):
                json_str = json_str[3:-3]
            
            suggestions_data = json.loads(json_str)
            return [OptimizationSuggestion(**suggestion) for suggestion in suggestions_data]
        except (json.JSONDecodeError, Exception):
            return [OptimizationSuggestion(
                section="skills",
                type="add_keyword",
                original="Current skills",
                suggested="Add missing job-required skills",
                reason="Failed to parse AI suggestions",
                impact="medium"
            )]

    def _get_existing_skills(self, resume_data: dict) -> set[str]:
        """Extract and normalize all existing skills from resume"""
        skills = resume_data.get('skills', {})
        existing_skills = set()
        
        # Collect skills from all categories
        for category in ['technical', 'soft_skills', 'tools', 'languages']:
            category_skills = skills.get(category, [])
            for skill in category_skills:
                existing_skills.add(skill.lower().strip())
        
        return existing_skills

    def _find_missing_skills(self, job_analysis: dict, existing_skills: set[str]) -> dict[str, list[str]]:
        """Find job requirements that don't exist in resume skills"""
        missing_skills = {}
        
        # Check required skills
        required_skills = job_analysis.get('required_skills', [])
        missing_required = [
            skill for skill in required_skills 
            if skill.lower().strip() not in existing_skills
        ]
        if missing_required:
            missing_skills['required_skills'] = missing_required
        
        # Check technologies
        technologies = job_analysis.get('technologies', [])
        missing_tech = [
            tech for tech in technologies 
            if tech.lower().strip() not in existing_skills
        ]
        if missing_tech:
            missing_skills['technologies'] = missing_tech
        
        return missing_skills

    async def _enhance_experience(
        self, resume_data: dict, job_analysis: dict
    ) -> list[OptimizationSuggestion]:
        """Generate experience enhancement suggestions"""
        
        experience_items = resume_data.get('experience', [])
        if not experience_items:
            return []

        first_experience = experience_items[0]
        
        prompt = f"""
        Enhance this work experience description to better match the job requirements.
        
        Job Title: {job_analysis.get('title', 'Target Role')}
        Job Requirements: {', '.join(job_analysis.get('key_requirements', []))}
        Required Technologies: {', '.join(job_analysis.get('technologies', []))}
        
        Current Experience:
        Title: {first_experience.get('title', '')}
        Company: {first_experience.get('company', '')}
        Description: {first_experience.get('description', [])}
        
        Return ONLY a JSON array with ONE suggestion:
        [
            {{
                "section": "experience",
                "type": "enhance_description",
                "original": "Current description bullet point",
                "suggested": "Enhanced description with quantified impact",
                "reason": "Better alignment with job requirements",
                "impact": "high"
            }}
        ]
        """

        messages = [{"role": "user", "content": prompt}]
        response_text = ""
        
        async for chunk in stream_llm_response(messages):
            response_text += chunk

        try:
            json_str = response_text.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:-3]
            elif json_str.startswith('```'):
                json_str = json_str[3:-3]
            
            suggestions_data = json.loads(json_str)
            return [OptimizationSuggestion(**suggestion) for suggestion in suggestions_data]
        except (json.JSONDecodeError, Exception):
            return [OptimizationSuggestion(
                section="experience",
                type="enhance_description",
                original="Current experience description",
                suggested="Enhanced description with quantified impact",
                reason="Improve alignment with job requirements",
                impact="high"
            )]


# Global service instance
optimization_service = OptimizationService()
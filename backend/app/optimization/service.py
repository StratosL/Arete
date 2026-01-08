import json
from typing import AsyncGenerator

from app.core.llm import stream_llm_response
from app.optimization.schemas import OptimizationProgress, OptimizationSuggestion


class OptimizationService:
    """Service for AI-powered resume optimization"""

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

        # Step 2: Generate keyword suggestions
        yield OptimizationProgress(
            step="keywords",
            progress=30,
            message="Identifying missing keywords...",
            suggestions=[],
            completed=False
        )

        keyword_suggestions = await self._generate_keyword_suggestions(resume_data, job_analysis)
        
        yield OptimizationProgress(
            step="keywords",
            progress=50,
            message="Generated keyword suggestions",
            suggestions=keyword_suggestions,
            completed=False
        )

        # Step 3: Enhance experience descriptions
        yield OptimizationProgress(
            step="experience",
            progress=70,
            message="Enhancing experience descriptions...",
            suggestions=keyword_suggestions,
            completed=False
        )

        experience_suggestions = await self._enhance_experience(resume_data, job_analysis)
        all_suggestions = keyword_suggestions + experience_suggestions

        yield OptimizationProgress(
            step="experience",
            progress=90,
            message="Enhanced experience descriptions",
            suggestions=all_suggestions,
            completed=False
        )

        # Step 4: Final optimization
        yield OptimizationProgress(
            step="complete",
            progress=100,
            message="Optimization complete",
            suggestions=all_suggestions,
            completed=True
        )

    async def _generate_keyword_suggestions(
        self, resume_data: dict, job_analysis: dict
    ) -> list[OptimizationSuggestion]:
        """Generate keyword optimization suggestions"""
        
        prompt = f"""
        Analyze this resume against job requirements and suggest keyword improvements.
        
        Job Requirements:
        - Required Skills: {', '.join(job_analysis.get('required_skills', []))}
        - Technologies: {', '.join(job_analysis.get('technologies', []))}
        - Key Requirements: {', '.join(job_analysis.get('key_requirements', []))}
        
        Resume Skills:
        - Technical: {', '.join(resume_data.get('skills', {}).get('technical', []))}
        - Frameworks: {', '.join(resume_data.get('skills', {}).get('frameworks', []))}
        
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
            # Clean and parse JSON
            json_str = response_text.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:-3]
            elif json_str.startswith('```'):
                json_str = json_str[3:-3]
            
            suggestions_data = json.loads(json_str)
            return [OptimizationSuggestion(**suggestion) for suggestion in suggestions_data]
        except (json.JSONDecodeError, Exception):
            # Fallback suggestion if parsing fails
            return [OptimizationSuggestion(
                section="skills",
                type="add_keyword",
                original="Current skills",
                suggested="Add missing job-required skills",
                reason="Failed to parse AI suggestions",
                impact="medium"
            )]

    async def _enhance_experience(
        self, resume_data: dict, job_analysis: dict
    ) -> list[OptimizationSuggestion]:
        """Generate experience enhancement suggestions"""
        
        experience_items = resume_data.get('experience', [])
        if not experience_items:
            return []

        # Take first experience item for optimization
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
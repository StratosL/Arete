import asyncio
import json
from typing import AsyncGenerator

from fastapi import HTTPException

from app.core.database import get_supabase_service_client
from app.core.llm import stream_llm_response
from app.optimization.schemas import (
    ATSScore,
    InterviewQuestion,
    KeywordMatchScore,
    OptimizationProgress,
    OptimizationSuggestion,
    SectionScore,
)


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

        # Calculate initial ATS score
        ats_score = self._calculate_ats_score(resume_data, job_analysis)

        # Step 1: Analyze alignment and show initial ATS score
        yield OptimizationProgress(
            step="analyzing",
            progress=10,
            message="Analyzing resume-job alignment...",
            suggestions=[],
            completed=False,
            ats_score=ats_score
        )
        await asyncio.sleep(1)

        # Step 2: Generate keyword suggestions
        yield OptimizationProgress(
            step="keywords",
            progress=30,
            message="Identifying missing keywords...",
            suggestions=[],
            completed=False,
            ats_score=ats_score
        )
        await asyncio.sleep(2)

        keyword_suggestions = await self._generate_keyword_suggestions(resume_data, job_analysis)

        yield OptimizationProgress(
            step="keywords",
            progress=50,
            message="Generated keyword suggestions",
            suggestions=keyword_suggestions,
            completed=False,
            ats_score=ats_score
        )
        await asyncio.sleep(1)

        # Step 3: Enhance experience descriptions
        yield OptimizationProgress(
            step="experience",
            progress=70,
            message="Enhancing experience descriptions...",
            suggestions=keyword_suggestions,
            completed=False,
            ats_score=ats_score
        )
        await asyncio.sleep(2)

        experience_suggestions = await self._enhance_experience(resume_data, job_analysis)
        all_suggestions = keyword_suggestions + experience_suggestions

        yield OptimizationProgress(
            step="experience",
            progress=85,
            message="Enhanced experience descriptions",
            suggestions=all_suggestions,
            completed=False,
            ats_score=ats_score
        )
        await asyncio.sleep(1)

        # Step 4: Generate interview questions
        yield OptimizationProgress(
            step="interview",
            progress=92,
            message="Generating interview preparation questions...",
            suggestions=all_suggestions,
            completed=False,
            ats_score=ats_score
        )
        await asyncio.sleep(1)

        interview_questions = await self._generate_interview_questions(resume_data, job_analysis)

        # Step 5: Final optimization complete
        suggestion_count = len(all_suggestions)
        question_count = len(interview_questions)
        completion_msg = (
            f"Optimization complete! Generated {suggestion_count} suggestions "
            f"and {question_count} interview questions."
        )
        yield OptimizationProgress(
            step="complete",
            progress=100,
            message=completion_msg,
            suggestions=all_suggestions,
            completed=True,
            ats_score=ats_score,
            interview_questions=interview_questions
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
                "suggested": "React, Node.js, Docker",
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

    def _calculate_ats_score(
        self, resume_data: dict, job_analysis: dict
    ) -> ATSScore:
        """Calculate ATS compatibility score based on resume-job alignment"""

        # Get existing skills and job requirements
        existing_skills = self._get_existing_skills(resume_data)

        # Calculate keyword match score (50% weight)
        required_skills = [s.lower().strip() for s in job_analysis.get('required_skills', [])]
        technologies = [t.lower().strip() for t in job_analysis.get('technologies', [])]
        all_required = list(set(required_skills + technologies))

        matched_keywords = [kw for kw in all_required if kw in existing_skills]
        missing_keywords = [kw for kw in all_required if kw not in existing_skills]

        total_keywords = len(all_required) if all_required else 1
        keyword_percentage = int((len(matched_keywords) / total_keywords) * 100)

        keyword_score = KeywordMatchScore(
            matched=len(matched_keywords),
            total=total_keywords,
            percentage=keyword_percentage,
            matched_keywords=matched_keywords[:10],  # Limit to top 10
            missing_keywords=missing_keywords[:10]   # Limit to top 10
        )

        # Calculate section completeness score (30% weight)
        sections = []
        section_checks = [
            ("Contact Info", bool(resume_data.get('personal_info', {}).get('email'))),
            ("Experience", len(resume_data.get('experience', [])) > 0),
            ("Skills", len(existing_skills) > 0),
            ("Education", len(resume_data.get('education', [])) > 0),
            ("Projects", len(resume_data.get('projects', [])) > 0),
        ]

        present_sections = 0
        for name, present in section_checks:
            score = 100 if present else 0
            sections.append(SectionScore(name=name, present=present, score=score))
            if present:
                present_sections += 1

        section_completeness = int((present_sections / len(section_checks)) * 100)

        # Calculate overall score (weighted)
        # Keyword match: 50%, Section completeness: 30%, Base structure: 20%
        base_score = 20  # Base points for having a parseable resume
        overall_score = int(
            (keyword_percentage * 0.5) +
            (section_completeness * 0.3) +
            base_score
        )
        overall_score = min(100, max(0, overall_score))  # Clamp to 0-100

        # Generate recommendations
        recommendations = []
        if keyword_percentage < 60:
            recommendations.append(
                f"Add {len(missing_keywords)} missing keywords to improve ATS matching"
            )
        if not resume_data.get('personal_info', {}).get('email'):
            recommendations.append("Add contact email for recruiter follow-up")
        if len(resume_data.get('experience', [])) == 0:
            recommendations.append("Add work experience section")
        if len(resume_data.get('projects', [])) == 0:
            recommendations.append("Add projects to showcase technical skills")
        if keyword_percentage >= 80 and section_completeness >= 80:
            recommendations.append("Resume is well-optimized for ATS systems")

        return ATSScore(
            overall_score=overall_score,
            keyword_match=keyword_score,
            section_completeness=section_completeness,
            sections=sections,
            recommendations=recommendations[:5]  # Limit to 5 recommendations
        )

    async def _generate_interview_questions(
        self, resume_data: dict, job_analysis: dict
    ) -> list[InterviewQuestion]:
        """Generate role-specific interview preparation questions"""

        job_title = job_analysis.get('title', 'Software Engineer')
        company = job_analysis.get('company', 'the company')
        technologies = job_analysis.get('technologies', [])[:5]
        requirements = job_analysis.get('key_requirements', [])[:3]
        experience_level = job_analysis.get('experience_level', 'mid-level')

        prompt = f"""
        Generate 5 interview preparation questions for a {experience_level} {job_title} role at {company}.

        Required Technologies: {', '.join(technologies)}
        Key Requirements: {', '.join(requirements)}

        Return ONLY a JSON array with exactly 5 questions in this format:
        [
            {{
                "category": "technical",
                "question": "Specific technical question about a required technology",
                "tips": "Brief tip for answering (1-2 sentences)"
            }},
            {{
                "category": "behavioral",
                "question": "Behavioral question using STAR method format",
                "tips": "Brief tip for answering"
            }},
            {{
                "category": "system_design",
                "question": "System design or architecture question",
                "tips": "Brief tip for answering"
            }},
            {{
                "category": "role_specific",
                "question": "Question specific to this role and company",
                "tips": "Brief tip for answering"
            }},
            {{
                "category": "technical",
                "question": "Another technical question about required skills",
                "tips": "Brief tip for answering"
            }}
        ]

        Make questions specific to the technologies and requirements listed.
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

            questions_data = json.loads(json_str)
            return [InterviewQuestion(**q) for q in questions_data[:5]]
        except (json.JSONDecodeError, Exception):
            # Return default questions if parsing fails
            return [
                InterviewQuestion(
                    category="technical",
                    question=f"Describe your experience with {technologies[0] if technologies else 'relevant technologies'}.",
                    tips="Use specific examples from past projects with metrics."
                ),
                InterviewQuestion(
                    category="behavioral",
                    question="Tell me about a challenging project and how you overcame obstacles.",
                    tips="Use the STAR method: Situation, Task, Action, Result."
                ),
                InterviewQuestion(
                    category="system_design",
                    question=f"How would you design a scalable system for {job_title} responsibilities?",
                    tips="Start with requirements, then discuss architecture and trade-offs."
                ),
                InterviewQuestion(
                    category="role_specific",
                    question=f"Why are you interested in the {job_title} role at {company}?",
                    tips="Research the company and connect your experience to their mission."
                ),
                InterviewQuestion(
                    category="technical",
                    question="Walk me through how you would debug a production issue.",
                    tips="Describe your systematic approach: logs, monitoring, isolation, fix."
                ),
            ]


# Global service instance
optimization_service = OptimizationService()
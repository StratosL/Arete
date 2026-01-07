import json
import uuid
import re
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.llm import get_llm_response


class JobAnalysisService:
    """Service for analyzing job descriptions"""
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def scrape_job_url(self, url: str) -> str:
        """Scrape job description from URL with retry logic"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(str(url), headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            raise Exception(f"Failed to scrape URL: {str(e)}")
    
    def _clean_job_text(self, text: str) -> str:
        """Clean and normalize job description text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\[\]]', ' ', text)
        # Limit length to prevent token overflow
        return text[:8000].strip()
    
    async def analyze_job_description(self, job_text: str) -> dict:
        """Analyze job description using Claude API"""
        
        cleaned_text = self._clean_job_text(job_text)
        
        prompt = f"""
        Analyze this job description and extract structured information. Return ONLY valid JSON.
        
        Job Description:
        {cleaned_text}
        
        Extract the following information in this exact JSON structure:
        {{
            "title": "Job title",
            "company": "Company name or 'Unknown' if not found",
            "required_skills": ["skill1", "skill2"],
            "preferred_skills": ["skill1", "skill2"],
            "technologies": ["tech1", "tech2"],
            "experience_level": "Entry/Mid/Senior/Lead/Executive",
            "key_requirements": ["requirement1", "requirement2"]
        }}
        
        Guidelines:
        - Extract technical skills, frameworks, programming languages
        - Separate required vs preferred/nice-to-have skills
        - Identify specific technologies mentioned
        - Determine experience level from years mentioned or role seniority
        - Include key qualifications and responsibilities
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = await get_llm_response(messages)
        
        try:
            # Clean response and parse JSON
            json_str = response.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:-3]
            elif json_str.startswith('```'):
                json_str = json_str[3:-3]
            
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")


# Global service instance
job_analysis_service = JobAnalysisService()
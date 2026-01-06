import json
import os
from typing import Optional

import pdfplumber
from docx import Document

from app.core.llm import get_llm_response

class ResumeParser:
    """Two-stage resume parser: File → Markdown → JSON"""
    
    async def parse_file(self, file_content: bytes, filename: str, github_url: Optional[str] = None) -> dict:
        """Parse resume file through two-stage process"""
        
        # Stage 1: Extract text to markdown
        if filename.endswith('.pdf'):
            markdown_text = self._parse_pdf(file_content)
        elif filename.endswith('.docx'):
            markdown_text = self._parse_docx(file_content)
        elif filename.endswith('.txt'):
            markdown_text = file_content.decode('utf-8')
        else:
            raise ValueError("Unsupported file format")
        
        # Stage 2: LLM processing to structured JSON
        structured_data = await self._markdown_to_json(markdown_text, github_url)
        
        return structured_data
    
    def _parse_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF and convert to markdown format"""
        import io
        
        markdown_lines = []
        
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Basic markdown formatting
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            # Detect headers (all caps, short lines)
                            if line.isupper() and len(line) < 50:
                                markdown_lines.append(f"## {line}")
                            else:
                                markdown_lines.append(line)
                    markdown_lines.append("")  # Page break
        
        return '\n'.join(markdown_lines)
    
    def _parse_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX and convert to markdown format"""
        import io
        
        doc = Document(io.BytesIO(file_content))
        markdown_lines = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                # Detect headers based on style or formatting
                if paragraph.style.name.startswith('Heading'):
                    markdown_lines.append(f"## {text}")
                else:
                    markdown_lines.append(text)
        
        return '\n'.join(markdown_lines)
    
    async def _markdown_to_json(self, markdown_text: str, github_url: Optional[str] = None) -> dict:
        """Convert markdown resume to structured JSON using LLM"""
        
        github_context = f"\nGitHub Profile: {github_url}" if github_url else ""
        
        prompt = f"""
        Parse this resume into structured JSON format. Extract all information accurately.
        
        Resume Text:
        {markdown_text}
        {github_context}
        
        Return ONLY valid JSON in this exact structure:
        {{
            "personal_info": {{
                "name": "Full Name",
                "email": "email@example.com",
                "phone": "phone number or null",
                "location": "city, state or null",
                "github": "github url or null",
                "linkedin": "linkedin url or null"
            }},
            "experience": [
                {{
                    "title": "Job Title",
                    "company": "Company Name",
                    "duration": "Start - End dates",
                    "description": ["bullet point 1", "bullet point 2"],
                    "technologies": ["tech1", "tech2"]
                }}
            ],
            "skills": {{
                "technical": ["skill1", "skill2"],
                "frameworks": ["framework1", "framework2"],
                "tools": ["tool1", "tool2"],
                "languages": ["language1", "language2"]
            }},
            "projects": [
                {{
                    "name": "Project Name",
                    "description": "Project description",
                    "technologies": ["tech1", "tech2"],
                    "github_url": "url or null",
                    "impact_metrics": ["metric1", "metric2"]
                }}
            ],
            "education": [
                {{
                    "degree": "Degree Type",
                    "institution": "School Name",
                    "graduation_year": "Year",
                    "gpa": "GPA or null"
                }}
            ]
        }}
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

# Global parser instance
resume_parser = ResumeParser()

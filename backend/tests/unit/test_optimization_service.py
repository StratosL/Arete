"""
Unit tests for optimization service
"""
import json
from unittest.mock import patch, Mock, AsyncMock
import pytest

from app.optimization.service import OptimizationService
from app.optimization.schemas import OptimizationSuggestion


class TestOptimizationService:
    """Test OptimizationService methods"""

    def setup_method(self):
        """Setup test fixtures"""
        self.service = OptimizationService()

    @pytest.mark.asyncio
    async def test_get_resume_job_data_success(self, mock_supabase, sample_resume_data, sample_job_analysis):
        """Test successful data retrieval"""
        # Mock resume response
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(
            data=[{"parsed_data": sample_resume_data}]
        )
        
        with patch('app.optimization.service.get_supabase_service_client', return_value=mock_supabase):
            resume_data, job_analysis = await self.service.get_resume_job_data("resume-123", "job-456")
            
            assert resume_data == sample_resume_data
            assert mock_supabase.table.called

    @pytest.mark.asyncio
    async def test_get_resume_job_data_resume_not_found(self, mock_supabase):
        """Test resume not found error"""
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
        
        with patch('app.optimization.service.get_supabase_service_client', return_value=mock_supabase):
            with pytest.raises(Exception, match="Resume not found"):
                await self.service.get_resume_job_data("invalid-resume", "job-456")

    @pytest.mark.asyncio
    async def test_save_optimization_success(self, mock_supabase):
        """Test successful optimization save"""
        optimized_data = {"test": "data"}
        
        with patch('app.optimization.service.get_supabase_service_client', return_value=mock_supabase):
            await self.service.save_optimization("resume-123", optimized_data)
            
            mock_supabase.table.assert_called_with("resumes")
            mock_supabase.table.return_value.update.assert_called_with({
                "optimized_data": optimized_data
            })

    @pytest.mark.asyncio
    async def test_generate_keyword_suggestions(self, sample_resume_data, sample_job_analysis):
        """Test keyword suggestion generation"""
        mock_response = json.dumps([{
            "section": "skills",
            "type": "add_keyword",
            "original": "Current skills",
            "suggested": "Enhanced skills with Docker",
            "reason": "Job requires Docker",
            "impact": "high"
        }])

        async def mock_stream_generator():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            suggestions = await self.service._generate_keyword_suggestions(sample_resume_data, sample_job_analysis)
            
            assert len(suggestions) == 1
            assert suggestions[0].section == "skills"
            assert suggestions[0].type == "add_keyword"
            assert suggestions[0].impact == "high"

    @pytest.mark.asyncio
    async def test_generate_keyword_suggestions_parse_error(self, sample_resume_data, sample_job_analysis):
        """Test keyword suggestion with JSON parse error"""
        async def mock_stream_generator():
            yield "Invalid JSON"

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            suggestions = await self.service._generate_keyword_suggestions(sample_resume_data, sample_job_analysis)
            
            # Should return fallback suggestion
            assert len(suggestions) == 1
            assert suggestions[0].reason == "Failed to parse AI suggestions"

    @pytest.mark.asyncio
    async def test_enhance_experience(self, sample_resume_data, sample_job_analysis):
        """Test experience enhancement"""
        mock_response = json.dumps([{
            "section": "experience",
            "type": "enhance_description",
            "original": "Built applications",
            "suggested": "Built scalable applications serving 10K+ users",
            "reason": "Added quantified impact",
            "impact": "high"
        }])

        async def mock_stream_generator():
            yield mock_response

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            suggestions = await self.service._enhance_experience(sample_resume_data, sample_job_analysis)
            
            assert len(suggestions) == 1
            assert suggestions[0].section == "experience"
            assert suggestions[0].type == "enhance_description"

    @pytest.mark.asyncio
    async def test_generate_cover_letter(self, sample_resume_data, sample_job_analysis):
        """Test cover letter generation"""
        mock_cover_letter = "Dear Hiring Manager,\n\nI am excited to apply for the Senior Python Developer position..."

        async def mock_stream_generator():
            yield mock_cover_letter

        with patch('app.optimization.service.stream_llm_response', return_value=mock_stream_generator()):
            result = await self.service.generate_cover_letter(sample_resume_data, sample_job_analysis)
            
            assert "Dear Hiring Manager" in result
            assert "Senior Python Developer" in result

    @pytest.mark.asyncio
    async def test_optimize_resume_full_flow(self, sample_resume_data, sample_job_analysis):
        """Test complete optimization flow"""
        with patch.object(self.service, '_generate_keyword_suggestions') as mock_keywords, \
             patch.object(self.service, '_enhance_experience') as mock_experience:
            
            mock_keywords.return_value = [OptimizationSuggestion(
                section="skills", type="add_keyword", original="Python", 
                suggested="Python, Docker", reason="Missing Docker", impact="high"
            )]
            mock_experience.return_value = [OptimizationSuggestion(
                section="experience", type="enhance_description", original="Built apps",
                suggested="Built scalable apps", reason="Added impact", impact="medium"
            )]
            
            progress_updates = []
            async for progress in self.service.optimize_resume(sample_resume_data, sample_job_analysis):
                progress_updates.append(progress)
            
            assert len(progress_updates) >= 4  # At least 4 progress updates
            assert progress_updates[-1].completed is True
            assert progress_updates[-1].progress == 100
            assert len(progress_updates[-1].suggestions) == 2
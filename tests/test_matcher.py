"""
Tests for CVMatcher main class.
"""

import pytest
from unittest.mock import Mock, patch
from cv_matcher import CVMatcher
from cv_matcher.models import CVAnalysis, MatchScore, FormattingAdvice


class TestCVMatcher:
    """Tests for CVMatcher class."""

    def test_init_no_api_key(self):
        """Test that initialization fails without API key."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                CVMatcher()

    def test_init_with_api_key(self):
        """Test successful initialization with API key."""
        matcher = CVMatcher(api_key="test-key")
        assert matcher.ai_analyzer.api_key == "test-key"

    def test_get_score_color(self):
        """Test score color determination."""
        matcher = CVMatcher(api_key="test-key")
        assert matcher._get_score_color(85) == "green"
        assert matcher._get_score_color(65) == "yellow"
        assert matcher._get_score_color(45) == "orange"
        assert matcher._get_score_color(25) == "red"

    @patch("cv_matcher.matcher.PDFParser.extract_text")
    @patch("cv_matcher.matcher.JobDescriptionFetcher.fetch")
    @patch("cv_matcher.matcher.AIAnalyzer.analyze")
    def test_analyze_cv_success(self, mock_analyze, mock_fetch, mock_extract):
        """Test successful CV analysis."""
        # Setup mocks
        mock_extract.return_value = "CV content"
        mock_fetch.return_value = "Job description"

        mock_score = MatchScore(
            overall_score=75.0,
            skills_match=80.0,
            experience_match=70.0,
            education_match=65.0,
            keywords_match=85.0,
        )
        mock_advice = FormattingAdvice(
            strengths=["Good"], weaknesses=["Improve"], suggestions=["Add more"]
        )
        mock_analysis = CVAnalysis(
            match_score=mock_score,
            formatting_advice=mock_advice,
            summary="Good match",
            recommendation="Apply",
        )
        mock_analyze.return_value = mock_analysis

        # Test
        matcher = CVMatcher(api_key="test-key")
        result = matcher.analyze_cv("test.pdf", "job description")

        assert result.match_score.overall_score == 75.0
        assert result.summary == "Good match"
        mock_extract.assert_called_once()
        mock_fetch.assert_called_once()
        mock_analyze.assert_called_once()

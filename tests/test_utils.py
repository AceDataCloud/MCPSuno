"""Unit tests for utility functions."""

from core.utils import (
    format_audio_result,
    format_lyrics_result,
    format_persona_result,
    format_task_result,
)


class TestFormatAudioResult:
    """Tests for format_audio_result function."""

    def test_format_success(self, mock_audio_response):
        """Test formatting successful audio response."""
        result = format_audio_result(mock_audio_response)
        assert "Task ID: test-task-123" in result
        assert "Trace ID: test-trace-456" in result
        assert "Song 1" in result
        assert "Test Song" in result
        assert "120.50s" in result
        assert "succeeded" in result
        assert "https://cdn1.suno.ai/test-audio.mp3" in result

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_audio_result(mock_error_response)
        assert "Error: invalid_request" in result
        assert "Invalid parameters" in result

    def test_format_empty_data(self):
        """Test formatting response with no audio data."""
        response = {"success": True, "task_id": "123", "data": []}
        result = format_audio_result(response)
        assert "Task ID: 123" in result
        assert "Song" not in result


class TestFormatLyricsResult:
    """Tests for format_lyrics_result function."""

    def test_format_success(self, mock_lyrics_response):
        """Test formatting successful lyrics response."""
        result = format_lyrics_result(mock_lyrics_response)
        assert "Task ID: lyrics-task-123" in result
        assert "Title: Test Song Title" in result
        assert "Status: complete" in result
        assert "Generated lyrics here" in result

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_lyrics_result(mock_error_response)
        assert "Error:" in result


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response):
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        assert "Task ID: task-123" in result
        assert "Action: generate" in result
        assert "Response: Success" in result
        assert "Test Song" in result

    def test_format_error(self):
        """Test formatting error response."""
        error_response = {"error": {"code": "not_found", "message": "Task not found"}}
        result = format_task_result(error_response)
        assert "Error: not_found" in result


class TestFormatPersonaResult:
    """Tests for format_persona_result function."""

    def test_format_success(self, mock_persona_response):
        """Test formatting successful persona response."""
        result = format_persona_result(mock_persona_response)
        assert "Persona Created Successfully" in result
        assert "persona-id-456" in result
        assert "generate_with_persona" in result

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_persona_result(mock_error_response)
        assert "Error:" in result

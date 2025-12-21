"""
Test suite for the Robotics Book RAG Chatbot backend.
Run with: pytest test_backend.py -v
"""

import pytest
import json
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test that health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns documentation info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "endpoints" in data


class TestChatEndpoint:
    """Test chat endpoint"""
    
    @patch('rag_agent.rag_agent.answer_question')
    def test_chat_success(self, mock_answer):
        """Test successful chat request"""
        mock_answer.return_value = {
            "answer": "ROS 2 is the Robot Operating System",
            "sources": [],
            "query": "What is ROS 2?",
            "selected_text": None,
        }
        
        response = client.post(
            "/api/chat",
            json={
                "query": "What is ROS 2?",
                "selected_text": None,
                "conversation_history": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "query" in data
    
    def test_chat_empty_query(self):
        """Test chat with empty query"""
        response = client.post(
            "/api/chat",
            json={
                "query": "",
                "selected_text": None,
                "conversation_history": []
            }
        )
        
        assert response.status_code == 400
        assert "detail" in response.json()
    
    @patch('rag_agent.rag_agent.answer_question')
    def test_chat_with_selected_text(self, mock_answer):
        """Test chat with selected text"""
        selected_text = "ROS 2 is a middleware platform"
        mock_answer.return_value = {
            "answer": "This refers to...",
            "sources": [],
            "query": "Explain this",
            "selected_text": selected_text,
        }
        
        response = client.post(
            "/api/chat",
            json={
                "query": "Explain this",
                "selected_text": selected_text,
                "conversation_history": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["selected_text"] == selected_text
    
    @patch('rag_agent.rag_agent.answer_question')
    def test_chat_with_conversation_history(self, mock_answer):
        """Test chat with conversation history"""
        history = [
            {
                "role": "user",
                "content": "What is ROS 2?"
            },
            {
                "role": "assistant",
                "content": "ROS 2 is..."
            }
        ]
        
        mock_answer.return_value = {
            "answer": "Continued explanation...",
            "sources": [],
            "query": "Tell me more",
            "selected_text": None,
        }
        
        response = client.post(
            "/api/chat",
            json={
                "query": "Tell me more",
                "selected_text": None,
                "conversation_history": history
            }
        )
        
        assert response.status_code == 200
        mock_answer.assert_called_once()
        # Verify conversation history was passed
        call_kwargs = mock_answer.call_args[1]
        assert call_kwargs["conversation_history"] == history


class TestSummarizeEndpoint:
    """Test summarize endpoint"""
    
    @patch('rag_agent.rag_agent.summarize_chapter')
    def test_summarize_success(self, mock_summarize):
        """Test successful summarize request"""
        mock_summarize.return_value = "This chapter covers..."
        
        response = client.get("/api/summarize/chapter-01")
        
        assert response.status_code == 200
        data = response.json()
        assert "chapter" in data
        assert "summary" in data
    
    @patch('rag_agent.rag_agent.summarize_chapter')
    def test_summarize_not_found(self, mock_summarize):
        """Test summarize with non-existent chapter"""
        mock_summarize.return_value = "No content found for chapter"
        
        response = client.get("/api/summarize/invalid-chapter")
        
        assert response.status_code == 200
        data = response.json()
        assert "No content found" in data["summary"]


class TestAdminEndpoints:
    """Test admin endpoints"""
    
    @patch('background_tasks.add_task')
    def test_background_indexing(self, mock_task):
        """Test background indexing"""
        # Create BackgroundTasks for testing
        from fastapi import BackgroundTasks
        
        response = client.post("/api/admin/index")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "started"
    
    @patch('document_indexer.index_robotics_book')
    def test_sync_indexing(self, mock_index):
        """Test synchronous indexing"""
        mock_index.return_value = {
            "total_files": 10,
            "indexed_files": 10,
            "total_chunks": 50,
            "errors": [],
            "success": True
        }
        
        response = client.get("/api/admin/index/sync")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "stats" in data


class TestErrorHandling:
    """Test error handling"""
    
    @patch('rag_agent.rag_agent.answer_question')
    def test_api_error_handling(self, mock_answer):
        """Test API error handling"""
        mock_answer.side_effect = Exception("API Error")
        
        response = client.post(
            "/api/chat",
            json={
                "query": "Test query",
                "selected_text": None,
                "conversation_history": []
            }
        )
        
        assert response.status_code == 500
        assert "detail" in response.json()


class TestCORSHeaders:
    """Test CORS headers"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present"""
        response = client.options("/api/chat")
        # CORS headers should be present in response
        assert "access-control-allow-origin" in response.headers or \
               "Access-Control-Allow-Origin" in response.headers


# Integration Tests

class TestIntegration:
    """Integration tests"""
    
    @patch('vector_store.vector_store.search_similar')
    @patch('rag_agent.rag_agent.client.chat.completions.create')
    @patch('database.db_manager.save_interaction')
    def test_full_chat_flow(self, mock_save, mock_llm, mock_search):
        """Test full chat flow"""
        # Mock search results
        mock_search.return_value = [
            {
                "score": 0.95,
                "content": "Sample content",
                "title": "Sample Title",
                "chapter": "Chapter 1",
                "source_url": "/docs/intro"
            }
        ]
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Sample answer"
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_llm.return_value = mock_response
        
        mock_save.return_value = 1
        
        response = client.post(
            "/api/chat",
            json={
                "query": "What is ROS?",
                "selected_text": None,
                "conversation_history": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Sample answer"
        assert len(data["sources"]) > 0


# Performance Tests

class TestPerformance:
    """Performance tests"""
    
    @patch('rag_agent.rag_agent.answer_question')
    def test_response_time(self, mock_answer):
        """Test response time is acceptable"""
        import time
        
        mock_answer.return_value = {
            "answer": "Quick response",
            "sources": [],
            "query": "Test",
            "selected_text": None,
        }
        
        start = time.time()
        response = client.post(
            "/api/chat",
            json={
                "query": "Test query",
                "selected_text": None,
                "conversation_history": []
            }
        )
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 10  # Should respond within 10 seconds


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

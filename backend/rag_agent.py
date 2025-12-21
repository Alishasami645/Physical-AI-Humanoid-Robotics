from openai import OpenAI
from vector_store import vector_store
from database import db_manager
from config import settings
from typing import Optional, List, Dict, Any
import json


class RAGAgent:
    """RAG (Retrieval-Augmented Generation) Agent using OpenRouter or OpenAI."""
    
    def __init__(self):
        if settings.use_openrouter and settings.openrouter_api_key:
            # Use OpenRouter with OpenAI-compatible client
            self.client = OpenAI(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_api_base
            )
            self.model = settings.openrouter_model
        else:
            # Fallback to OpenAI
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.model_name
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the agent."""
        return """You are an expert assistant for a comprehensive robotics and humanoid robotics book.
Your role is to help readers understand concepts, provide detailed explanations, and answer questions about:
- Physical AI and embodied intelligence
- ROS 2 architecture and robotics nervous systems
- Digital twins and simulation (Gazebo, Unity)
- NVIDIA Isaac for AI robot brains
- Vision-Language-Action (VLA) models
- Autonomous humanoid systems

Guidelines:
1. Base your answers primarily on the provided context from the book
2. If context is limited, acknowledge this and provide relevant background knowledge
3. For questions about selected text, focus on explaining that specific passage
4. Provide clear, educational explanations suitable for robotics learners
5. When applicable, reference specific chapters or concepts from the book
6. Be honest if a topic is outside the book's scope
7. Use technical terminology accurately while remaining accessible

Always cite the source when referencing book content."""

    def _apply_personalization(self, user_profile: Optional[Dict[str, Any]]) -> str:
        """Build personalization suffix based on user profile."""
        if not user_profile:
            return ""
        
        parts = []
        sb = user_profile.get("software_background")
        he = user_profile.get("hardware_experience")
        langs = user_profile.get("programming_languages")
        goal = user_profile.get("learning_goal")
        
        if sb:
            parts.append(f"Adjust explanations for a {sb} software background.")
        if he:
            parts.append(f"Consider hardware experience level: {he}.")
        if langs:
            if isinstance(langs, str):
                parts.append(f"Prefer code examples in: {langs}.")
            else:
                parts.append(f"Prefer code examples in: {', '.join(langs)}.")
        if goal:
            parts.append(f"Learning Goal: {goal}.")
        
        if parts:
            return "\n\nPersonalization guidance:\n" + "\n".join(parts)
        return ""
    
    def answer_question(self, query: str, selected_text: Optional[str] = None,
                       conversation_history: Optional[List[Dict]] = None, 
                       user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Answer user question using RAG.
        
        Args:
            query: The user's question
            selected_text: Optional text selected by the user
            conversation_history: Previous messages for context
            user_profile: Optional user personalization profile
        
        Returns:
            Dictionary with answer and metadata
        """
        
        # Retrieve relevant documents
        if selected_text:
            # Search based on selected text
            relevant_docs = vector_store.search_by_selected_text(selected_text)
        else:
            # Search based on query
            relevant_docs = vector_store.search_similar(query)
        
        # Build context from retrieved documents
        context = self._build_context(relevant_docs)
        
        # Prepare messages
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add context and current query with personalization
        user_message = self._build_user_message(query, selected_text, context, user_profile)
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            system=self.system_prompt,
            temperature=0.7,
            max_tokens=1500,
        )
        
        answer = response.choices[0].message.content
        
        # Save interaction to database
        db_manager.save_interaction(
            user_query=query,
            assistant_response=answer,
            selected_text=selected_text,
            metadata={
                "num_sources": len(relevant_docs),
                "model": self.model,
                "personalized": user_profile is not None,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                }
            }
        )
        
        return {
            "answer": answer,
            "sources": relevant_docs,
            "query": query,
            "selected_text": selected_text,
        }
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents."""
        if not documents:
            return "No relevant context found in the knowledge base."
        
        context_parts = ["Based on the book content:\n"]
        
        for i, doc in enumerate(documents, 1):
            title = doc.get("title", "Unknown")
            chapter = doc.get("chapter", "")
            content = doc.get("content", "")[:500]  # Truncate for token efficiency
            score = doc.get("score", 0)
            
            context_parts.append(
                f"\n[Source {i}] {title} (Chapter: {chapter}, Relevance: {score:.2f})\n"
                f"Content: {content}..."
            )
        
        return "\n".join(context_parts)
    
    def _build_user_message(self, query: str, selected_text: Optional[str],
                           context: str, user_profile: Optional[Dict[str, Any]] = None) -> str:
        """Build the user message with context and personalization."""
        message_parts = [context, "\n\n---\n\n"]
        
        if selected_text:
            message_parts.append(
                f"The user has selected the following text from the book:\n"
                f"\"{selected_text}\"\n\n"
            )
        
        message_parts.append(f"User Question: {query}")
        
        # Add personalization guidance
        personalization = self._apply_personalization(user_profile)
        message_parts.append(personalization)
        
        return "".join(message_parts)
    
    def summarize_chapter(self, chapter_name: str) -> str:
        """Generate a summary for a specific chapter."""
        docs = db_manager.get_documents_by_chapter(chapter_name)
        
        if not docs:
            return f"No content found for chapter: {chapter_name}"
        
        combined_content = "\n\n".join([doc["content"] for doc in docs])[:3000]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"""Please provide a comprehensive summary of the following chapter content 
                    from a robotics book. Focus on key concepts and learning outcomes.
                    
                    Content:
                    {combined_content}"""
                }
            ],
            temperature=0.5,
            max_tokens=800,
        )
        
        return response.choices[0].message.content


# Global RAG agent instance
rag_agent = RAGAgent()

from typing import Optional, Dict, Any, List
from config import settings
from openai import OpenAI
from database import db_manager
from rag_agent import rag_agent


class UserPersonalizationAgent:
    """Manages user personalization data and applies it to chapter content and prompts."""

    def __init__(self):
        self.db = db_manager
        if settings.use_openrouter and settings.openrouter_api_key:
            self.client = OpenAI(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_api_base
            )
            self.model = settings.openrouter_model
        else:
            self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
            self.model = settings.model_name

    def save_profile(self, external_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update a user profile. Returns saved profile from DB."""
        user = None
        if external_id:
            user = self.db.get_user_by_external_id(external_id)

        if user:
            # update
            self.db.update_user_profile(user["id"], profile)
            return self.db.get_user_by_id(user["id"])
        else:
            user_id = self.db.create_user(
                external_id=external_id,
                email=profile.get("email"),
                software_background=profile.get("software_background"),
                hardware_experience=profile.get("hardware_experience"),
                programming_languages=profile.get("programming_languages"),
                learning_goal=profile.get("learning_goal"),
                metadata=profile.get("metadata"),
            )
            return self.db.get_user_by_id(user_id)

    def apply_personalization(self, user_profile: Dict[str, Any], prompt: str) -> str:
        """Modify the given prompt according to user profile (difficulty, examples)."""
        parts = []
        if not user_profile:
            return prompt

        sb = user_profile.get("software_background")
        he = user_profile.get("hardware_experience")
        langs = user_profile.get("programming_languages")
        goal = user_profile.get("learning_goal")

        if sb:
            parts.append(f"Adjust explanations for a {sb} software background.")
        if he:
            parts.append(f"Consider hardware experience level: {he}.")
        if langs:
            parts.append(f"Prefer code examples in: {', '.join(langs)}.")
        if goal:
            parts.append(f"Learning Goal: {goal}.")

        return "\n".join(parts) + "\n" + prompt

    def personalize_chapter(self, chapter_content: str, user_profile: Dict[str, Any]) -> str:
        """Personalize entire chapter based on user skill level, hardware experience, languages, and learning goal."""
        if not self.client or not user_profile:
            return chapter_content

        software_level = user_profile.get("software_background", "beginner")
        hardware_exp = user_profile.get("hardware_experience", "low")
        languages = ", ".join(user_profile.get("programming_languages", [])) if user_profile.get("programming_languages") else "none"
        goal = user_profile.get("learning_goal", "general understanding")

        prompt = f"""You are an expert robotics educator. Personalize this chapter for a learner with:
- Software level: {software_level}
- Hardware experience: {hardware_exp}
- Programming languages: {languages}
- Learning goal: {goal}

Rules:
1. For beginner: Use simpler language, add more explanations, include real-world analogies
2. For intermediate: Assume basic knowledge, add practical applications
3. For advanced: Include cutting-edge techniques, theoretical depth, optimization
4. Preserve ALL markdown formatting, headings, code blocks, and structure
5. Only adapt explanatory text and examples to match the profile
6. Keep code blocks exactly as-is

Chapter:\n{chapter_content}

Return ONLY the personalized chapter with no explanations."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Personalization error: {str(e)}")
            return chapter_content


class ChapterContextAgent:
    """Provides chapter-specific context and learning outcomes using RAG."""

    def __init__(self):
        self.db = db_manager
        self.rag = rag_agent
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = settings.model_name

    def get_chapter_context(self, chapter_name: str) -> Dict[str, Any]:
        """Get comprehensive chapter context including summary, concepts, and prerequisites."""
        docs = self.db.get_documents_by_chapter(chapter_name)
        
        context = {
            "chapter": chapter_name,
            "document_count": len(docs) if docs else 0,
            "summary": self.rag.summarize_chapter(chapter_name) if docs else None,
        }
        
        # Extract metadata if available
        if self.client and docs:
            context["metadata"] = self._extract_chapter_metadata(chapter_name, docs)
        
        return context

    def _extract_chapter_metadata(self, chapter_name: str, docs: List[Dict]) -> Dict[str, Any]:
        """Extract key concepts, learning outcomes, and difficulty level."""
        content_sample = "\n".join([d.get("content", "")[:500] for d in docs[:3]])
        
        prompt = f"""Analyze this chapter and extract metadata as JSON:

Chapter: {chapter_name}
Content: {content_sample}

Return ONLY a JSON object (no markdown):
{{
    "key_concepts": ["list", "of", "concepts"],
    "learning_outcomes": ["what students will learn"],
    "prerequisites": ["prior knowledge needed"],
    "difficulty": "beginner|intermediate|advanced"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            import json
            return json.loads(response.choices[0].message.content)
        except:
            return {
                "key_concepts": [],
                "learning_outcomes": [],
                "prerequisites": [],
                "difficulty": "intermediate"
            }


class TranslationAgent:
    """Translate content to Urdu while preserving code blocks, headings, and format."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = settings.model_name

    def translate_to_urdu(self, content: str) -> str:
        """Translate markdown content to professional Urdu.
        
        Preserves:
        - All code blocks (``` ... ```) in English
        - All markdown headings (# ## ### etc)
        - All formatting (bold, italic, lists)
        - Technical terms (adds English in brackets)
        """
        print(f"[TranslationAgent] Starting translation. Content length: {len(content)}")
        print(f"[TranslationAgent] OpenAI client available: {self.client is not None}")
        
        # If no OpenAI client configured, use a lightweight fallback to LibreTranslate
        # while preserving code blocks and headings.
        if not self.client:
            print("[TranslationAgent] Using LibreTranslate fallback (no OpenAI key)")
            try:
                import re
                import requests

                # Extract code blocks and headings to protect them from translation
                code_blocks = []
                def code_repl(m):
                    code_blocks.append(m.group(0))
                    return f"__CODE_BLOCK_{len(code_blocks)-1}__"

                content_protected = re.sub(r'```[\s\S]*?```', code_repl, content)
                print(f"[TranslationAgent] Extracted {len(code_blocks)} code blocks")

                headings = []
                def heading_repl(m):
                    headings.append(m.group(0))
                    return f"__HEADING_{len(headings)-1}__"

                content_protected = re.sub(r'^\s{0,3}#{1,6}.*$', heading_repl, content_protected, flags=re.MULTILINE)
                print(f"[TranslationAgent] Extracted {len(headings)} headings")

                # Call LibreTranslate public instance
                print("[TranslationAgent] Calling LibreTranslate API...")
                try:
                    resp = requests.post(
                        'https://libretranslate.de/translate',
                        json={
                            'q': content_protected,
                            'source': 'en',
                            'target': 'ur',
                            'format': 'text'
                        },
                        timeout=20
                    )
                    print(f"[TranslationAgent] LibreTranslate response status: {resp.status_code}")
                    if resp.status_code == 200:
                        translated = resp.json().get('translatedText', '')
                        print(f"[TranslationAgent] Translation successful, output length: {len(translated)}")
                    else:
                        print(f"[TranslationAgent] LibreTranslate error: {resp.status_code} - {resp.text}")
                        return content
                except Exception as e:
                    print(f"[TranslationAgent] LibreTranslate request error: {str(e)}")
                    return content

                # Restore headings and code blocks
                def restore_heading(m):
                    idx = int(m.group(1))
                    return headings[idx] if idx < len(headings) else m.group(0)

                def restore_code(m):
                    idx = int(m.group(1))
                    return code_blocks[idx] if idx < len(code_blocks) else m.group(0)

                translated = re.sub(r'__HEADING_(\d+)__', restore_heading, translated)
                translated = re.sub(r'__CODE_BLOCK_(\d+)__', restore_code, translated)
                print(f"[TranslationAgent] Restored code blocks and headings")

                return translated
            except Exception as e:
                print(f"[TranslationAgent] Fallback translation error: {e}")
                import traceback
                traceback.print_exc()
                return content

        print("[TranslationAgent] Using OpenAI for translation")
        prompt = f"""Translate this markdown to professional Urdu. Follow these rules precisely:

1. PRESERVE all markdown formatting: headings (#, ##, ###), bold (**), italic (*), lists
2. DO NOT translate code blocks (``` ... ```). Keep code in English exactly as-is
3. DO NOT translate headings - keep them in English
4. For technical robotics terms without good Urdu equivalents, keep in English [in brackets]
5. Translate only the explanatory prose, descriptions, and commentary
6. Keep the document structure identical

Content to translate:
{content}

Return ONLY the translated markdown with no additional text or explanations."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=4000
            )
            result = response.choices[0].message.content
            print(f"[TranslationAgent] OpenAI translation successful, output length: {len(result)}")
            return result
        except Exception as e:
            print(f"[TranslationAgent] OpenAI translation error: {str(e)}")
            import traceback
            traceback.print_exc()
            return content

    def translate_section(self, title: str, content: str) -> Dict[str, str]:
        """Translate a single section (title + content) and return both translations."""
        full_content = f"# {title}\n\n{content}"
        translated = self.translate_to_urdu(full_content)
        
        lines = translated.split("\n", 2)
        title_urdu = lines[0].replace("# ", "").strip() if len(lines) > 0 else title
        content_urdu = lines[2] if len(lines) > 2 else translated
        
        return {
            "title_en": title,
            "title_urdu": title_urdu,
            "content_en": content,
            "content_urdu": content_urdu
        }


# Singleton agent instances to be reused across handlers
user_personalization_agent = UserPersonalizationAgent()
chapter_context_agent = ChapterContextAgent()
translation_agent = TranslationAgent()

"""AI helper for content generation and analysis using Claude."""

import os
from typing import Optional, List, Dict
from anthropic import Anthropic


class AIHelper:
    """Helper class for AI-powered content generation and analysis."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize AI helper.

        Args:
            api_key: Anthropic API key (defaults to env var)
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 4000, system: Optional[str] = None) -> str:
        """
        Generate content using Claude.

        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            system: System prompt

        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages
        }

        if system:
            kwargs["system"] = system

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def analyze_funnel(self, funnel_html: str, funnel_url: str) -> Dict:
        """
        Analyze a sales funnel to extract structure and copy.

        Args:
            funnel_html: HTML content of the funnel
            funnel_url: URL of the funnel

        Returns:
            Dictionary with funnel structure
        """
        prompt = f"""Analyze this sales funnel and extract the key components.

URL: {funnel_url}

HTML:
{funnel_html[:10000]}  # Limit HTML length

Extract and return in this format:
1. **Headline**: The main headline
2. **Subheadline**: Supporting text under headline
3. **Problem**: What pain point is being addressed
4. **Solution**: How the product solves it
5. **Bullet Points**: Key benefits/features (list them)
6. **Price**: Product price
7. **CTA**: Call-to-action text
8. **Testimonials**: Any social proof (summarize)
9. **Structure**: Overall funnel structure/flow

Be concise and extract only the marketing copy, not technical elements."""

        return self.generate(prompt, max_tokens=2000)

    def create_product_from_research(
        self,
        topic: str,
        research_data: List[str],
        format_type: str = "7-day protocol",
        tone: str = "casual",
        pages: int = 12
    ) -> str:
        """
        Create a product from research data.

        Args:
            topic: Product topic
            research_data: List of research content (transcripts, articles, etc.)
            format_type: Type of format (protocol, course, guide, etc.)
            tone: Writing tone
            pages: Target page count

        Returns:
            Generated product content
        """
        research_combined = "\n\n---\n\n".join(research_data)

        prompt = f"""Create a {format_type} on {topic} based on this research.

RESEARCH DATA:
{research_combined[:15000]}  # Limit research length

REQUIREMENTS:
- Format: {format_type}
- Tone: {tone}
- Target length: ~{pages} pages
- Make it actionable and structured
- Use checklists and step-by-step instructions
- Make it feel like a system, not a course
- Focus on practical implementation

Generate the complete content now."""

        system = f"""You are an expert content creator specializing in {topic}.
Create high-quality, actionable content that provides real value.
Structure it clearly with sections, checklists, and action items."""

        return self.generate(prompt, max_tokens=4000, system=system)

    def translate_content(
        self,
        content: str,
        target_language: str,
        content_type: str = "marketing copy"
    ) -> str:
        """
        Translate content while maintaining emotional intensity.

        Args:
            content: Content to translate
            target_language: Target language
            content_type: Type of content being translated

        Returns:
            Translated content
        """
        prompt = f"""Translate this {content_type} to {target_language}.

CRITICAL REQUIREMENTS:
- Maintain the same emotional intensity and persuasion
- Keep the same structure and formatting
- Adapt idioms naturally (don't translate literally)
- Preserve any formatting like bullets, numbers, headings
- Make it sound native, not robotic

CONTENT TO TRANSLATE:
{content}

Provide ONLY the translation, no explanations."""

        return self.generate(prompt, max_tokens=4000)

    def recreate_copy(
        self,
        original_copy: str,
        new_topic: str,
        new_language: Optional[str] = None
    ) -> str:
        """
        Recreate marketing copy for a different topic/language.

        Args:
            original_copy: Original marketing copy
            new_topic: New topic to adapt for
            new_language: Optional target language

        Returns:
            Recreated copy
        """
        lang_instruction = f" in {new_language}" if new_language else ""

        prompt = f"""Recreate this marketing copy for a different topic{lang_instruction}.

ORIGINAL COPY:
{original_copy}

NEW TOPIC: {new_topic}

REQUIREMENTS:
- Keep the exact same structure and flow
- Maintain the same emotional hooks
- Use similar length for each section
- Preserve the persuasion psychology
- Make it feel natural for the new topic

Generate the new copy now."""

        return self.generate(prompt, max_tokens=3000)

    def generate_testimonials(
        self,
        product_topic: str,
        num_testimonials: int = 5,
        language: str = "english"
    ) -> List[str]:
        """
        Generate realistic testimonial text (for placeholders/testing).

        Args:
            product_topic: Topic of the product
            num_testimonials: Number to generate
            language: Target language

        Returns:
            List of testimonial texts
        """
        prompt = f"""Generate {num_testimonials} realistic customer testimonials for a product about {product_topic} in {language}.

Requirements:
- Make them feel authentic and varied
- Include specific results/outcomes
- Different lengths (some short, some longer)
- Different customer personas
- Focus on transformation/results

Format as a numbered list."""

        response = self.generate(prompt, max_tokens=2000)

        # Simple split by newlines and clean up
        testimonials = [
            line.strip()
            for line in response.split("\n")
            if line.strip() and any(char.isalpha() for char in line)
        ]

        return testimonials[:num_testimonials]

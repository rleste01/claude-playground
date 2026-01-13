"""Generate product content from research."""

from typing import List, Dict, Optional
from ..utils.youtube_helper import YouTubeResearcher
from ..utils.ai_helper import AIHelper
import os


class ContentGenerator:
    """Generate digital product content using AI and research."""

    def __init__(self, ai_helper: Optional[AIHelper] = None):
        """
        Initialize content generator.

        Args:
            ai_helper: AI helper instance
        """
        self.ai_helper = ai_helper or AIHelper()
        self.youtube = YouTubeResearcher()

    def research_topic(
        self,
        topic: str,
        video_urls: Optional[List[str]] = None,
        num_videos: int = 4,
        min_views: int = 100000
    ) -> List[str]:
        """
        Research a topic using YouTube videos.

        Args:
            topic: Topic to research
            video_urls: Optional list of specific video URLs
            num_videos: Number of videos to research
            min_views: Minimum view count for videos

        Returns:
            List of transcripts
        """
        print(f"\n📚 Researching Topic: {topic}")

        if not video_urls:
            print(f"   ⚠️  No video URLs provided")
            print(f"   Search YouTube for: '{topic}'")
            print(f"   Find {num_videos} videos with {min_views:,}+ views")
            print(f"   Look for: doctors, experts, high-quality content")
            return []

        return self.youtube.research_topic(
            topic=topic,
            num_videos=num_videos,
            min_views=min_views,
            video_urls=video_urls
        )

    def generate_product(
        self,
        topic: str,
        research_data: List[str],
        format_type: str = "7-day protocol",
        tone: str = "casual",
        target_pages: int = 12
    ) -> str:
        """
        Generate a complete product from research.

        Args:
            topic: Product topic
            research_data: Research transcripts/content
            format_type: Product format (protocol, guide, course, etc.)
            tone: Writing tone
            target_pages: Target page count

        Returns:
            Generated product content
        """
        print(f"\n✍️  Generating Product")
        print(f"   Topic: {topic}")
        print(f"   Format: {format_type}")
        print(f"   Tone: {tone}")
        print(f"   Target Length: ~{target_pages} pages")

        if not research_data:
            raise ValueError("No research data provided")

        content = self.ai_helper.create_product_from_research(
            topic=topic,
            research_data=research_data,
            format_type=format_type,
            tone=tone,
            pages=target_pages
        )

        print(f"   ✓ Generated {len(content)} characters")

        return content

    def save_as_pdf(self, content: str, output_path: str) -> bool:
        """
        Save content as PDF.

        Args:
            content: Content to save
            output_path: Output file path

        Returns:
            True if successful

        Note: Requires proper PDF generation library for production.
        For now, saves as markdown with instructions.
        """
        # Save as markdown first
        md_path = output_path.replace('.pdf', '.md')

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n   ✓ Saved as Markdown: {md_path}")
        print(f"   📄 To convert to PDF:")
        print(f"      Option 1: Use https://www.notion.so (paste → export as PDF)")
        print(f"      Option 2: Use https://www.markdowntopdf.com")
        print(f"      Option 3: Install pandoc: pandoc {md_path} -o {output_path}")

        return True

    def create_from_youtube(
        self,
        topic: str,
        video_urls: List[str],
        output_path: str,
        format_type: str = "7-day protocol",
        tone: str = "casual"
    ) -> str:
        """
        Complete pipeline: research YouTube → generate product → save.

        Args:
            topic: Product topic
            video_urls: List of YouTube video URLs to research
            output_path: Where to save the product
            format_type: Product format
            tone: Writing tone

        Returns:
            Generated content
        """
        # Step 1: Research
        transcripts = self.research_topic(topic, video_urls)

        if not transcripts:
            raise ValueError("Failed to get transcripts from YouTube videos")

        # Step 2: Generate
        content = self.generate_product(
            topic=topic,
            research_data=transcripts,
            format_type=format_type,
            tone=tone
        )

        # Step 3: Save
        self.save_as_pdf(content, output_path)

        return content

    def enhance_with_checklist(self, content: str) -> str:
        """
        Add checklists and actionable elements to content.

        Args:
            content: Original content

        Returns:
            Enhanced content with checklists
        """
        prompt = f"""Take this content and enhance it with actionable checklists.

ORIGINAL CONTENT:
{content}

REQUIREMENTS:
- Add daily/weekly checklists where appropriate
- Make it more actionable and step-by-step
- Add checkboxes ([ ]) for action items
- Maintain the original structure and information
- Keep the same tone

Return the enhanced version."""

        enhanced = self.ai_helper.generate(prompt, max_tokens=4000)

        return enhanced

    def create_supplement_guide(self, main_topic: str, content: str) -> str:
        """
        Generate a supplementary guide (e.g., supplement recommendations).

        Args:
            main_topic: Main product topic
            content: Main product content

        Returns:
            Supplementary guide content
        """
        prompt = f"""Create a supplementary guide for optional supplements/tools related to {main_topic}.

MAIN CONTENT CONTEXT:
{content[:2000]}

Create a guide covering:
1. Optional supplements/tools (clearly mark as OPTIONAL)
2. What each does and why it helps
3. Recommended dosages/usage
4. Where to find them
5. Cost estimates

Keep it practical and evidence-based. Tone: helpful but not pushy."""

        supplement_guide = self.ai_helper.generate(prompt, max_tokens=2000)

        return supplement_guide

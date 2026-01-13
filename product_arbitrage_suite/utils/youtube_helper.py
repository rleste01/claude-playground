"""YouTube research utilities."""

import requests
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
import re


class YouTubeResearcher:
    """Research topics using YouTube videos."""

    def __init__(self):
        """Initialize YouTube researcher."""
        pass

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.

        Args:
            url: YouTube URL

        Returns:
            Video ID or None
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',
            r'youtube\.com\/embed\/([^&\n?]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def get_transcript(self, video_url: str, language: str = 'en') -> str:
        """
        Get transcript for a YouTube video.

        Args:
            video_url: YouTube video URL
            language: Language code (en, fr, de, etc.)

        Returns:
            Video transcript as text
        """
        video_id = self.extract_video_id(video_url)

        if not video_id:
            raise ValueError(f"Invalid YouTube URL: {video_url}")

        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=[language]
            )

            # Combine all text
            full_transcript = ' '.join([item['text'] for item in transcript_list])
            return full_transcript

        except Exception as e:
            raise Exception(f"Failed to get transcript for {video_url}: {str(e)}")

    def search_videos(
        self,
        query: str,
        min_views: int = 100000,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for YouTube videos on a topic.

        Args:
            query: Search query
            min_views: Minimum view count
            max_results: Maximum number of results

        Returns:
            List of video information dictionaries

        Note: This requires YouTube Data API key for production use.
        For now, returns manual search instructions.
        """
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

        print(f"\n🔍 YouTube Video Research")
        print(f"   Query: {query}")
        print(f"   Min Views: {min_views:,}")
        print(f"   Search URL: {search_url}")
        print(f"\n   Manual Steps:")
        print(f"   1. Visit the search URL above")
        print(f"   2. Sort by view count")
        print(f"   3. Find {max_results} videos with {min_views:,}+ views")
        print(f"   4. Look for videos from doctors/experts")
        print(f"   5. Copy video URLs")

        return [
            {
                'query': query,
                'search_url': search_url,
                'instructions': f'Find {max_results} videos with {min_views:,}+ views',
                'note': 'For automated search, implement with YouTube Data API v3'
            }
        ]

    def research_topic(
        self,
        topic: str,
        num_videos: int = 4,
        min_views: int = 100000,
        video_urls: Optional[List[str]] = None
    ) -> List[str]:
        """
        Research a topic by collecting transcripts from multiple videos.

        Args:
            topic: Topic to research
            num_videos: Number of videos to analyze
            min_views: Minimum view count for videos
            video_urls: Optional list of specific video URLs to use

        Returns:
            List of transcripts
        """
        if not video_urls:
            print(f"\n📚 Researching: {topic}")
            print(f"   Need {num_videos} video URLs with {min_views:,}+ views")
            print(f"   Search YouTube for: '{topic}'")
            return []

        transcripts = []

        for i, url in enumerate(video_urls[:num_videos], 1):
            try:
                print(f"   [{i}/{num_videos}] Extracting transcript from: {url}")
                transcript = self.get_transcript(url)
                transcripts.append(transcript)
                print(f"   ✓ Extracted {len(transcript)} characters")
            except Exception as e:
                print(f"   ✗ Failed: {str(e)}")

        return transcripts

    def get_video_info(self, video_url: str) -> Dict:
        """
        Get basic video information.

        Args:
            video_url: YouTube video URL

        Returns:
            Video information dictionary

        Note: Requires YouTube Data API for full implementation.
        """
        video_id = self.extract_video_id(video_url)

        return {
            'video_id': video_id,
            'url': video_url,
            'note': 'Full metadata requires YouTube Data API v3'
        }

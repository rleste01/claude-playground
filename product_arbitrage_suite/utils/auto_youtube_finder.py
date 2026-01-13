"""Automated YouTube video discovery and selection."""

from typing import List, Dict, Optional
from youtubesearchpython import VideosSearch
import scrapetube
from datetime import datetime, timedelta
import re


class AutomatedYouTubeFinder:
    """Automatically discover and select high-quality YouTube videos for research."""

    def __init__(
        self,
        min_views: int = 100000,
        max_age_days: int = 730,
        prefer_expert_channels: bool = True
    ):
        """
        Initialize YouTube finder.

        Args:
            min_views: Minimum view count
            max_age_days: Maximum video age in days
            prefer_expert_channels: Prioritize expert/doctor channels
        """
        self.min_views = min_views
        self.max_age_days = max_age_days
        self.prefer_expert_channels = prefer_expert_channels

        # Keywords that indicate expert channels
        self.expert_keywords = [
            'dr', 'doctor', 'phd', 'md', 'professor', 'expert',
            'scientist', 'researcher', 'clinic', 'university'
        ]

    def find_videos(
        self,
        topic: str,
        num_videos: int = 4,
        require_captions: bool = True
    ) -> List[Dict]:
        """
        Find high-quality videos on a topic.

        Args:
            topic: Topic to search for
            num_videos: Number of videos to find
            require_captions: Only return videos with captions

        Returns:
            List of video data dictionaries
        """
        print(f"\n📹 Finding YouTube Videos")
        print(f"   Topic: {topic}")
        print(f"   Minimum Views: {self.min_views:,}")
        print(f"   Required Videos: {num_videos}")

        # Search for videos
        search_results = self._search_videos(topic, limit=num_videos * 5)

        # Filter and rank videos
        qualified_videos = self._filter_and_rank_videos(search_results)

        # Select best videos
        selected_videos = qualified_videos[:num_videos]

        print(f"   ✓ Found {len(selected_videos)} qualifying videos")

        return selected_videos

    def _search_videos(self, topic: str, limit: int = 20) -> List[Dict]:
        """Search YouTube for videos."""
        try:
            print(f"      🔍 Searching YouTube...")
            # Use youtubesearchpython for initial search
            search = VideosSearch(topic, limit=limit)
            results = search.result()

            videos = []

            for video in results.get('result', []):
                video_data = {
                    'video_id': video.get('id'),
                    'url': f"https://www.youtube.com/watch?v={video.get('id')}",
                    'title': video.get('title'),
                    'channel': video.get('channel', {}).get('name', ''),
                    'views': self._parse_view_count(video.get('viewCount', {}).get('text', '0')),
                    'duration': video.get('duration'),
                    'published': video.get('publishedTime', ''),
                    'description': video.get('descriptionSnippet', [{}])[0].get('text', ''),
                }

                videos.append(video_data)

            print(f"      ✓ Found {len(videos)} videos")
            return videos

        except Exception as e:
            print(f"   ⚠️ Warning: Search failed: {str(e)}")
            return []

    def _filter_and_rank_videos(self, videos: List[Dict]) -> List[Dict]:
        """Filter videos by criteria and rank by quality."""
        print(f"      📊 Filtering and ranking {len(videos)} videos...")
        qualified = []

        for video in videos:
            # Check minimum views
            if video['views'] < self.min_views:
                continue

            # Calculate quality score
            score = self._calculate_quality_score(video)
            video['quality_score'] = score

            qualified.append(video)

        # Sort by quality score
        qualified.sort(key=lambda x: x['quality_score'], reverse=True)

        print(f"      ✓ {len(qualified)} videos passed quality filters")
        return qualified

    def _calculate_quality_score(self, video: Dict) -> float:
        """Calculate quality score for a video."""
        score = 0.0

        # View count (normalized)
        views = video['views']
        score += min(views / 1000000, 10)  # Up to 10 points for 1M+ views

        # Expert channel bonus
        if self.prefer_expert_channels:
            channel_name = video['channel'].lower()
            title = video['title'].lower()

            if any(keyword in channel_name or keyword in title for keyword in self.expert_keywords):
                score += 5  # Bonus for expert channels

        # Recency bonus (videos from last 2 years preferred)
        published_text = video.get('published', '').lower()
        if 'month' in published_text or 'week' in published_text:
            score += 2
        elif 'year' in published_text:
            years_match = re.search(r'(\d+)', published_text)
            if years_match:
                years = int(years_match.group(1))
                if years <= 1:
                    score += 1

        # Length bonus (longer videos = more content)
        duration = video.get('duration', '')
        if duration:
            minutes = self._parse_duration_to_minutes(duration)
            if 10 <= minutes <= 60:  # Sweet spot: 10-60 minutes
                score += 3
            elif minutes > 60:
                score += 2

        return score

    def _parse_view_count(self, view_text: str) -> int:
        """Parse view count from text like '1.2M views'."""
        try:
            # Remove non-numeric characters except decimal points
            view_text = view_text.lower().replace(',', '').replace(' views', '')

            if 'k' in view_text:
                number = float(view_text.replace('k', ''))
                return int(number * 1000)
            elif 'm' in view_text:
                number = float(view_text.replace('m', ''))
                return int(number * 1000000)
            elif 'b' in view_text:
                number = float(view_text.replace('b', ''))
                return int(number * 1000000000)
            else:
                return int(float(view_text))

        except Exception:
            return 0

    def _parse_duration_to_minutes(self, duration: str) -> int:
        """Parse duration string to minutes."""
        try:
            # Format: "12:34" or "1:23:45"
            parts = duration.split(':')

            if len(parts) == 2:  # MM:SS
                return int(parts[0])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 60 + int(parts[1])

            return 0

        except Exception:
            return 0

    def get_alternative_searches(self, topic: str) -> List[str]:
        """Generate alternative search queries for better results."""
        alternatives = [
            f"how to {topic}",
            f"{topic} guide",
            f"{topic} explained",
            f"{topic} tutorial",
            f"fix {topic}",
            f"improve {topic}",
            f"{topic} tips",
            f"{topic} advice",
        ]

        return alternatives

    def find_videos_multi_query(
        self,
        topic: str,
        num_videos: int = 4
    ) -> List[Dict]:
        """
        Find videos using multiple search queries for better coverage.

        Args:
            topic: Topic to search for
            num_videos: Number of videos to find

        Returns:
            List of best videos across all queries
        """
        print(f"\n📹 Multi-Query Video Discovery")
        print(f"   Topic: {topic}")

        all_videos = []
        seen_ids = set()

        # Try main query
        print(f"   🎯 Main search: '{topic}'")
        main_results = self._search_videos(topic, limit=20)
        for video in main_results:
            if video['video_id'] not in seen_ids:
                all_videos.append(video)
                seen_ids.add(video['video_id'])

        # Try alternative queries
        alternatives = self.get_alternative_searches(topic)[:3]  # Try top 3 alternatives
        print(f"   🔄 Trying {len(alternatives)} alternative searches...")

        for i, alt_query in enumerate(alternatives, 1):
            print(f"   {i}. '{alt_query}'")
            alt_results = self._search_videos(alt_query, limit=10)

            for video in alt_results:
                if video['video_id'] not in seen_ids:
                    all_videos.append(video)
                    seen_ids.add(video['video_id'])

        print(f"   📦 Collected {len(all_videos)} unique videos total")

        # Filter and rank all collected videos
        qualified_videos = self._filter_and_rank_videos(all_videos)

        # Select best ones
        selected = qualified_videos[:num_videos]

        print(f"   ✓ Selected {len(selected)} top videos")

        for i, video in enumerate(selected, 1):
            print(f"      {i}. {video['title']}")
            print(f"         Channel: {video['channel']}")
            print(f"         Views: {video['views']:,}")
            print(f"         Score: {video['quality_score']:.1f}")

        return selected

    def export_video_urls(self, videos: List[Dict]) -> List[str]:
        """
        Export just the URLs from video data.

        Args:
            videos: List of video data dictionaries

        Returns:
            List of YouTube URLs
        """
        return [video['url'] for video in videos]


# Convenience function
def auto_find_youtube_videos(
    topic: str,
    num_videos: int = 4,
    min_views: int = 100000
) -> List[str]:
    """
    Automatically find and return YouTube video URLs for a topic.

    Args:
        topic: Topic to research
        num_videos: Number of videos to find
        min_views: Minimum view count

    Returns:
        List of YouTube video URLs
    """
    finder = AutomatedYouTubeFinder(min_views=min_views)
    videos = finder.find_videos_multi_query(topic, num_videos)
    return finder.export_video_urls(videos)

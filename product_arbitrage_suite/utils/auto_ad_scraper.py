"""Automated Facebook Ad Library scraper using Playwright."""

import asyncio
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
from datetime import datetime, timedelta
import re
import json


class AutomatedAdScraper:
    """Automatically scrape Facebook Ad Library for winning ads."""

    FB_AD_LIBRARY_URL = "https://www.facebook.com/ads/library"

    def __init__(self, headless: bool = True):
        """
        Initialize automated ad scraper.

        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def start(self):
        """Start browser instance."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()

    async def close(self):
        """Close browser instance."""
        if self.browser:
            await self.browser.close()

    async def search_ads(
        self,
        keyword: str,
        country: str = "US",
        min_days_running: int = 14,
        max_results: int = 20
    ) -> List[Dict]:
        """
        Search for ads in Facebook Ad Library.

        Args:
            keyword: Search keyword
            country: Country code
            min_days_running: Minimum days ad must be running
            max_results: Maximum number of ads to return

        Returns:
            List of ad data dictionaries
        """
        if not self.page:
            await self.start()

        print(f"\n🔍 Scraping Facebook Ad Library")
        print(f"   Keyword: {keyword}")
        print(f"   Country: {country}")
        print(f"   Min Days: {min_days_running}")

        # Build search URL
        search_url = (
            f"{self.FB_AD_LIBRARY_URL}/"
            f"?active_status=active"
            f"&ad_type=all"
            f"&country={country}"
            f"&q={keyword.replace(' ', '+')}"
            f"&sort_data[direction]=desc"
            f"&sort_data[mode]=relevancy_monthly_grouped"
        )

        try:
            # Navigate to search page
            print(f"   Loading: {search_url}")
            await self.page.goto(search_url, wait_until="networkidle", timeout=30000)

            # Wait for results to load
            await self.page.wait_for_selector('[data-testid="search-results"]', timeout=10000)

            # Scroll to load more results
            await self._scroll_to_load_more(max_scrolls=5)

            # Extract ad cards
            ads = await self._extract_ads(min_days_running, max_results)

            print(f"   ✓ Found {len(ads)} qualifying ads")

            return ads

        except Exception as e:
            print(f"   ✗ Error scraping: {str(e)}")
            return []

    async def _scroll_to_load_more(self, max_scrolls: int = 5):
        """Scroll page to load more results."""
        for i in range(max_scrolls):
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

    async def _extract_ads(self, min_days_running: int, max_results: int) -> List[Dict]:
        """Extract ad data from loaded page."""
        ads = []

        # Get all ad containers
        ad_containers = await self.page.query_selector_all('[data-testid="ad-card"]')

        for container in ad_containers[:max_results * 2]:  # Get extra in case some don't qualify
            try:
                ad_data = await self._extract_single_ad(container)

                if ad_data and ad_data.get('days_running', 0) >= min_days_running:
                    ads.append(ad_data)

                if len(ads) >= max_results:
                    break

            except Exception as e:
                print(f"   Warning: Failed to extract ad: {str(e)}")
                continue

        return ads

    async def _extract_single_ad(self, container) -> Optional[Dict]:
        """Extract data from a single ad container."""
        ad_data = {
            'timestamp': datetime.now().isoformat(),
            'ad_copy': '',
            'landing_page_url': '',
            'started_running': None,
            'days_running': 0,
            'image_urls': [],
            'video_url': None,
        }

        # Extract ad copy
        copy_element = await container.query_selector('[data-testid="ad-preview-message"]')
        if copy_element:
            ad_data['ad_copy'] = await copy_element.inner_text()

        # Extract started running date
        date_element = await container.query_selector('[data-testid="ad-library-start-date"]')
        if date_element:
            date_text = await date_element.inner_text()
            ad_data['started_running'] = date_text
            ad_data['days_running'] = self._parse_days_running(date_text)

        # Extract landing page URL
        link_element = await container.query_selector('a[href*="http"]')
        if link_element:
            ad_data['landing_page_url'] = await link_element.get_attribute('href')

        # Extract images
        image_elements = await container.query_selector_all('img[src*="scontent"]')
        for img in image_elements:
            src = await img.get_attribute('src')
            if src:
                ad_data['image_urls'].append(src)

        # Extract video (if present)
        video_element = await container.query_selector('video source')
        if video_element:
            ad_data['video_url'] = await video_element.get_attribute('src')

        return ad_data

    def _parse_days_running(self, date_text: str) -> int:
        """Parse days running from date text."""
        try:
            # Handle various date formats from Facebook
            # "Started running on Dec 1, 2024"
            # "Started 26 days ago"

            if "ago" in date_text.lower():
                # Extract number of days
                match = re.search(r'(\d+)\s+days?\s+ago', date_text, re.IGNORECASE)
                if match:
                    return int(match.group(1))

            elif "started running on" in date_text.lower():
                # Parse actual date
                date_match = re.search(r'on\s+(\w+\s+\d+,\s+\d{4})', date_text, re.IGNORECASE)
                if date_match:
                    date_str = date_match.group(1)
                    start_date = datetime.strptime(date_str, "%b %d, %Y")
                    days_running = (datetime.now() - start_date).days
                    return days_running

            return 0

        except Exception:
            return 0

    async def get_ad_details(self, ad_url: str) -> Dict:
        """
        Get detailed information about a specific ad.

        Args:
            ad_url: Facebook ad library URL for the ad

        Returns:
            Detailed ad information
        """
        if not self.page:
            await self.start()

        try:
            await self.page.goto(ad_url, wait_until="networkidle", timeout=30000)

            # Extract detailed information
            details = {
                'url': ad_url,
                'full_copy': '',
                'cta_text': '',
                'engagement_metrics': {},
            }

            # Add more detailed scraping here as needed

            return details

        except Exception as e:
            print(f"Error getting ad details: {str(e)}")
            return {}


# Sync wrapper for easier use
def scrape_winning_ads(
    keyword: str,
    country: str = "US",
    min_days_running: int = 14,
    max_results: int = 20
) -> List[Dict]:
    """
    Synchronous wrapper for scraping ads.

    Args:
        keyword: Search keyword
        country: Country code
        min_days_running: Minimum days running
        max_results: Maximum results

    Returns:
        List of ad data
    """
    async def _scrape():
        async with AutomatedAdScraper() as scraper:
            return await scraper.search_ads(
                keyword=keyword,
                country=country,
                min_days_running=min_days_running,
                max_results=max_results
            )

    return asyncio.run(_scrape())

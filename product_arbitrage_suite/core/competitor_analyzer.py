"""Automated competitor analysis in target markets."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from urllib.parse import quote_plus
import time


class CompetitorAnalyzer:
    """Analyze competitors in target markets."""

    def __init__(self, ai_helper=None):
        """
        Initialize competitor analyzer.

        Args:
            ai_helper: AI helper instance for analysis
        """
        self.ai_helper = ai_helper
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def analyze_market(
        self,
        niche: str,
        language: str,
        dialect: Optional[str] = None,
        max_competitors: int = 20
    ) -> Dict:
        """
        Analyze competitors in a specific market.

        Args:
            niche: Product niche
            language: Target language
            dialect: Language dialect
            max_competitors: Maximum competitors to analyze

        Returns:
            Competitor analysis dictionary
        """
        print(f"\n🔍 Competitor Analysis")
        print(f"   Niche: {niche}")
        print(f"   Market: {language} ({dialect or 'standard'})")

        analysis = {
            'niche': niche,
            'language': language,
            'dialect': dialect,
            'timestamp': time.time(),
            'competitors': [],
            'total_found': 0,
            'avg_price': 0,
            'price_range': {'min': 999, 'max': 0},
            'common_formats': [],
            'market_saturation': 'unknown',
            'opportunity_score': 0,
        }

        # Search Google in target language
        print(f"   🔍 Searching Google in {language}...")
        competitors = self._search_google_competitors(niche, language, max_competitors)
        analysis['competitors'] = competitors
        analysis['total_found'] = len(competitors)
        print(f"   ✓ Found {len(competitors)} Google results")

        # Search Gumroad
        print(f"   🛍️ Searching Gumroad...")
        gumroad_competitors = self._search_gumroad(niche, language)
        analysis['competitors'].extend(gumroad_competitors)
        print(f"   ✓ Found {len(gumroad_competitors)} Gumroad products")

        # Analyze pricing
        prices = [c['price'] for c in analysis['competitors'] if c.get('price')]
        if prices:
            analysis['avg_price'] = sum(prices) / len(prices)
            analysis['price_range']['min'] = min(prices)
            analysis['price_range']['max'] = max(prices)

        # Determine market saturation
        analysis['market_saturation'] = self._calculate_saturation(len(analysis['competitors']))

        # Calculate opportunity score
        analysis['opportunity_score'] = self._calculate_opportunity_score(analysis)

        print(f"   ✓ Found {len(analysis['competitors'])} competitors")
        print(f"   Saturation: {analysis['market_saturation']}")
        print(f"   Opportunity Score: {analysis['opportunity_score']}/10")

        if analysis['avg_price'] > 0:
            print(f"   Avg Price: {analysis['avg_price']:.2f}")

        return analysis

    def _search_google_competitors(
        self,
        niche: str,
        language: str,
        max_results: int = 20
    ) -> List[Dict]:
        """Search Google for competitors."""
        competitors = []

        # Build search query in target language
        search_terms = self._get_search_terms(niche, language)
        print(f"      🔎 Trying {len(search_terms[:3])} search variations...")

        for i, search_term in enumerate(search_terms[:3], 1):  # Try top 3 search variations
            try:
                print(f"      {i}. \"{search_term}\"")
                results = self._google_search(search_term, language, limit=10)
                competitors.extend(results)
                print(f"         ✓ Found {len(results)} results")

                if len(competitors) >= max_results:
                    break

                time.sleep(2)  # Be nice to Google

            except Exception as e:
                print(f"      ⚠️ Search failed: {str(e)}")
                continue

        # Deduplicate by URL
        seen_urls = set()
        unique_competitors = []

        for comp in competitors:
            url = comp.get('url', '')
            if url and url not in seen_urls:
                unique_competitors.append(comp)
                seen_urls.add(url)

        return unique_competitors[:max_results]

    def _google_search(self, query: str, language: str, limit: int = 10) -> List[Dict]:
        """Perform Google search."""
        # Note: This is a simplified version. For production, use Google Custom Search API
        # or a service like SerpAPI

        search_url = f"https://www.google.com/search?q={quote_plus(query)}&hl={language}"

        try:
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            results = []

            # Parse search results
            for result in soup.select('.g')[:limit]:
                title_elem = result.select_one('h3')
                link_elem = result.select_one('a')
                snippet_elem = result.select_one('.VwiC3b')

                if title_elem and link_elem:
                    competitor = {
                        'title': title_elem.get_text(),
                        'url': link_elem.get('href', ''),
                        'snippet': snippet_elem.get_text() if snippet_elem else '',
                        'price': self._extract_price(snippet_elem.get_text() if snippet_elem else ''),
                        'source': 'google',
                    }

                    results.append(competitor)

            return results

        except Exception as e:
            print(f"   Google search error: {str(e)}")
            return []

    def _search_gumroad(self, niche: str, language: str) -> List[Dict]:
        """Search Gumroad for competitors."""
        competitors = []

        try:
            # Gumroad search
            search_url = f"https://gumroad.com/discover?query={quote_plus(niche)}"

            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse Gumroad results (simplified)
            for product in soup.select('.product-card')[:10]:
                title_elem = product.select_one('.product-title')
                price_elem = product.select_one('.product-price')
                link_elem = product.select_one('a')

                if title_elem:
                    competitor = {
                        'title': title_elem.get_text(),
                        'url': link_elem.get('href', '') if link_elem else '',
                        'price': self._parse_price(price_elem.get_text() if price_elem else ''),
                        'source': 'gumroad',
                    }

                    competitors.append(competitor)

        except Exception as e:
            print(f"   Gumroad search error: {str(e)}")

        return competitors

    def _get_search_terms(self, niche: str, language: str) -> List[str]:
        """Generate search terms in target language."""
        # This is simplified - ideally translate these terms properly
        search_patterns = [
            f"{niche} guide",
            f"{niche} pdf",
            f"how to {niche}",
            f"{niche} ebook",
            f"{niche} course",
        ]

        return search_patterns

    def _extract_price(self, text: str) -> Optional[float]:
        """Extract price from text."""
        if not text:
            return None

        # Look for common price patterns
        price_patterns = [
            r'[\$€£R\$]\s*(\d+(?:[.,]\d{2})?)',
            r'(\d+(?:[.,]\d{2})?)\s*[\$€£]',
        ]

        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '.')
                try:
                    return float(price_str)
                except ValueError:
                    continue

        return None

    def _parse_price(self, price_text: str) -> Optional[float]:
        """Parse price from text."""
        return self._extract_price(price_text)

    def _calculate_saturation(self, num_competitors: int) -> str:
        """Calculate market saturation level."""
        if num_competitors < 5:
            return "very_low"
        elif num_competitors < 10:
            return "low"
        elif num_competitors < 20:
            return "medium"
        elif num_competitors < 40:
            return "high"
        else:
            return "very_high"

    def _calculate_opportunity_score(self, analysis: Dict) -> float:
        """Calculate opportunity score (0-10)."""
        score = 10.0

        # Penalize for high competition
        num_competitors = len(analysis['competitors'])

        if num_competitors < 5:
            score -= 0
        elif num_competitors < 10:
            score -= 1
        elif num_competitors < 20:
            score -= 3
        elif num_competitors < 40:
            score -= 5
        else:
            score -= 7

        # Bonus for clear pricing opportunity
        if analysis['avg_price'] > 0:
            if analysis['avg_price'] < 20:
                score += 1  # Room to price higher
            elif analysis['avg_price'] > 50:
                score += 1  # Can undercut

        return max(0, min(score, 10))

    def compare_markets(
        self,
        niche: str,
        markets: List[Dict]
    ) -> List[Dict]:
        """
        Compare the same niche across multiple markets.

        Args:
            niche: Product niche
            markets: List of market configs (language, dialect)

        Returns:
            List of market analyses sorted by opportunity
        """
        print(f"\n🌍 Comparing Markets for: {niche}")

        analyses = []

        for market in markets:
            analysis = self.analyze_market(
                niche=niche,
                language=market['language'],
                dialect=market.get('dialect')
            )

            analyses.append(analysis)

            time.sleep(2)  # Rate limiting

        # Sort by opportunity score
        analyses.sort(key=lambda x: x['opportunity_score'], reverse=True)

        print(f"\n   Top Opportunities:")
        for i, analysis in enumerate(analyses[:5], 1):
            lang = analysis['language']
            dialect = f" ({analysis['dialect']})" if analysis['dialect'] else ""
            score = analysis['opportunity_score']
            competitors = len(analysis['competitors'])

            print(f"   {i}. {lang.title()}{dialect}: {score:.1f}/10 ({competitors} competitors)")

        return analyses

    def get_pricing_recommendation(
        self,
        competitor_analysis: Dict,
        market_multiplier: float = 1.0
    ) -> Dict:
        """
        Get pricing recommendation based on competitor analysis.

        Args:
            competitor_analysis: Analysis from analyze_market()
            market_multiplier: Price multiplier for local market

        Returns:
            Pricing recommendation
        """
        avg_price = competitor_analysis.get('avg_price', 27)
        price_range = competitor_analysis.get('price_range', {'min': 17, 'max': 47})

        # Calculate recommended price
        if avg_price > 0:
            # Aim for slightly below average to be competitive
            recommended = avg_price * 0.85
        else:
            # No competitors found, use default
            recommended = 27

        # Apply market multiplier
        recommended *= market_multiplier

        # Round to preferred ending
        preferred_endings = [7, 9, 97, 99]
        final_price = recommended

        for ending in preferred_endings:
            if ending < 10:  # Single digit endings (7, 9)
                candidate = int(recommended / 10) * 10 + ending
            else:  # Two digit endings (97, 99)
                candidate = int(recommended / 100) * 100 + ending

            if abs(candidate - recommended) < abs(final_price - recommended):
                final_price = candidate

        return {
            'recommended_price': final_price,
            'competitor_avg': avg_price,
            'competitor_range': price_range,
            'rationale': f"Priced {((avg_price - final_price) / avg_price * 100):.0f}% below average to be competitive",
        }

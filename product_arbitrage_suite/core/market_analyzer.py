"""Analyze market gaps and opportunities."""

from typing import Dict, List
import json


class MarketAnalyzer:
    """Analyze markets to find opportunities for product arbitrage."""

    # Common info product niches
    NICHES = [
        'sleep',
        'productivity',
        'fitness',
        'weight loss',
        'relationships',
        'dating',
        'money',
        'investing',
        'business',
        'side hustle',
        'mental health',
        'anxiety',
        'confidence',
        'communication',
        'parenting',
    ]

    # Target markets
    MARKETS = {
        'english': {'code': 'en', 'countries': ['US', 'UK', 'CA', 'AU'], 'saturation': 'high'},
        'french': {'code': 'fr', 'countries': ['FR', 'BE', 'CH', 'CA'], 'saturation': 'medium'},
        'german': {'code': 'de', 'countries': ['DE', 'AT', 'CH'], 'saturation': 'medium'},
        'spanish': {'code': 'es', 'countries': ['ES', 'MX', 'AR', 'CO'], 'saturation': 'medium'},
        'italian': {'code': 'it', 'countries': ['IT'], 'saturation': 'low'},
        'portuguese': {'code': 'pt', 'countries': ['PT', 'BR'], 'saturation': 'low'},
    }

    def __init__(self):
        """Initialize market analyzer."""
        pass

    def analyze_gap(self, niche: str, target_market: str = 'french') -> Dict:
        """
        Analyze market gap for a niche in a target market.

        Args:
            niche: Product niche
            target_market: Target market/language

        Returns:
            Gap analysis results
        """
        print(f"\n📊 Market Gap Analysis")
        print(f"   Niche: {niche}")
        print(f"   Target Market: {target_market}")

        market_info = self.MARKETS.get(target_market, {})

        analysis = {
            'niche': niche,
            'target_market': target_market,
            'market_info': market_info,
            'opportunity_score': self._calculate_opportunity_score(niche, target_market),
            'research_needed': self._get_research_instructions(niche, target_market),
        }

        self._print_analysis(analysis)

        return analysis

    def _calculate_opportunity_score(self, niche: str, target_market: str) -> int:
        """
        Calculate opportunity score (1-10).

        Args:
            niche: Product niche
            target_market: Target market

        Returns:
            Score from 1-10
        """
        market_info = self.MARKETS.get(target_market, {})
        saturation = market_info.get('saturation', 'high')

        # Base score on market saturation
        score_map = {
            'low': 8,
            'medium': 7,
            'high': 5,
        }

        base_score = score_map.get(saturation, 5)

        # High-demand niches get a boost
        high_demand_niches = ['sleep', 'productivity', 'fitness', 'money', 'anxiety']
        if niche in high_demand_niches:
            base_score += 1

        return min(base_score, 10)

    def _get_research_instructions(self, niche: str, target_market: str) -> Dict:
        """Get instructions for researching the market gap."""

        market_info = self.MARKETS.get(target_market, {})
        language = target_market
        countries = market_info.get('countries', [])

        return {
            'steps': [
                f"1. Search Google in {language}: '{niche}' + 'guide', 'protocol', 'method'",
                f"2. Search Facebook Ad Library in {', '.join(countries[:2])}",
                f"3. Check Gumroad, Etsy for existing products in {language}",
                "4. Count competitors (goal: <10 quality products)",
                "5. Check prices (opportunity if yours is priced right)",
            ],
            'tools': [
                f"Google.com (change language to {market_info.get('code', '')})",
                "Facebook Ad Library",
                "Gumroad",
                "Etsy",
            ],
            'ideal_result': f"Found <10 quality products in {language} market",
        }

    def _print_analysis(self, analysis: Dict):
        """Print analysis results."""
        print(f"\n   Opportunity Score: {analysis['opportunity_score']}/10")
        print(f"   Market Saturation: {analysis['market_info'].get('saturation', 'unknown')}")
        print(f"\n   📋 Research Steps:")

        for step in analysis['research_needed']['steps']:
            print(f"      {step}")

        print(f"\n   Ideal Result: {analysis['research_needed']['ideal_result']}")

    def compare_markets(self, niche: str) -> List[Dict]:
        """
        Compare opportunity across all markets for a niche.

        Args:
            niche: Product niche

        Returns:
            List of market opportunities sorted by score
        """
        print(f"\n🌍 Comparing Markets for: {niche}")

        opportunities = []

        for market in self.MARKETS.keys():
            if market == 'english':
                continue  # Skip English (source market)

            score = self._calculate_opportunity_score(niche, market)

            opportunities.append({
                'market': market,
                'score': score,
                'saturation': self.MARKETS[market]['saturation'],
                'countries': self.MARKETS[market]['countries'],
            })

        # Sort by score
        opportunities.sort(key=lambda x: x['score'], reverse=True)

        # Print results
        print(f"\n   Top Markets:")
        for i, opp in enumerate(opportunities[:5], 1):
            print(f"   {i}. {opp['market'].title()}: {opp['score']}/10 "
                  f"({opp['saturation']} saturation)")

        return opportunities

    def estimate_revenue(
        self,
        price: float,
        daily_budget: float,
        cpa: float = 10,
        conversion_rate: float = 0.03
    ) -> Dict:
        """
        Estimate revenue potential.

        Args:
            price: Product price
            daily_budget: Daily ad budget
            cpa: Cost per acquisition
            conversion_rate: Landing page conversion rate

        Returns:
            Revenue estimates
        """
        clicks_per_day = daily_budget / (cpa / (conversion_rate * 100))
        sales_per_day = clicks_per_day * conversion_rate
        revenue_per_day = sales_per_day * price
        profit_per_day = revenue_per_day - daily_budget

        monthly = {
            'revenue': revenue_per_day * 30,
            'ad_spend': daily_budget * 30,
            'profit': profit_per_day * 30,
            'sales': sales_per_day * 30,
        }

        print(f"\n💰 Revenue Estimate")
        print(f"   Product Price: ${price}")
        print(f"   Daily Ad Budget: ${daily_budget}")
        print(f"   Estimated CPA: ${cpa}")
        print(f"   Conversion Rate: {conversion_rate:.1%}")
        print(f"\n   Monthly Results:")
        print(f"   Revenue: ${monthly['revenue']:,.2f}")
        print(f"   Ad Spend: ${monthly['ad_spend']:,.2f}")
        print(f"   Profit: ${monthly['profit']:,.2f}")
        print(f"   Sales: {monthly['sales']:.0f}")

        return {
            'daily': {
                'revenue': revenue_per_day,
                'ad_spend': daily_budget,
                'profit': profit_per_day,
                'sales': sales_per_day,
            },
            'monthly': monthly,
        }

    def suggest_niches(self, target_market: str = 'french') -> List[Dict]:
        """
        Suggest niches with best opportunities in target market.

        Args:
            target_market: Target market

        Returns:
            List of niche suggestions sorted by opportunity
        """
        print(f"\n💡 Niche Suggestions for {target_market.title()} Market")

        suggestions = []

        for niche in self.NICHES:
            score = self._calculate_opportunity_score(niche, target_market)
            suggestions.append({
                'niche': niche,
                'score': score,
            })

        suggestions.sort(key=lambda x: x['score'], reverse=True)

        print(f"\n   Top 5 Niches:")
        for i, sugg in enumerate(suggestions[:5], 1):
            print(f"   {i}. {sugg['niche'].title()}: {sugg['score']}/10")

        return suggestions

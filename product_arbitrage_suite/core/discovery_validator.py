"""Discovery and validation stage - test products with minimal spend."""

from typing import Dict, Optional
from datetime import datetime, timedelta
import json
import os


class DiscoveryValidator:
    """Run low-spend tests to validate product-market fit before full launch."""

    def __init__(
        self,
        daily_budget: float = 15,
        test_duration_days: int = 3,
        min_clicks: int = 50
    ):
        """
        Initialize discovery validator.

        Args:
            daily_budget: Daily ad budget for testing
            test_duration_days: How many days to test
            min_clicks: Minimum clicks needed for valid test
        """
        self.daily_budget = daily_budget
        self.test_duration_days = test_duration_days
        self.min_clicks = min_clicks

        # Success thresholds
        self.min_ctr = 0.02  # 2% click-through rate
        self.max_cpa = 15  # Max cost per acquisition
        self.min_conversion_rate = 0.01  # 1% landing page conversion

    def create_test_plan(
        self,
        niche: str,
        target_market: str,
        estimated_cpc: float = 0.5
    ) -> Dict:
        """
        Create a low-spend test plan.

        Args:
            niche: Product niche
            target_market: Target market/language
            estimated_cpc: Estimated cost per click

        Returns:
            Test plan dictionary
        """
        total_budget = self.daily_budget * self.test_duration_days
        estimated_clicks = total_budget / estimated_cpc

        plan = {
            'niche': niche,
            'target_market': target_market,
            'daily_budget': self.daily_budget,
            'total_budget': total_budget,
            'test_duration_days': self.test_duration_days,
            'estimated_cpc': estimated_cpc,
            'estimated_clicks': int(estimated_clicks),
            'min_clicks_needed': self.min_clicks,
            'success_criteria': {
                'min_ctr': self.min_ctr,
                'max_cpa': self.max_cpa,
                'min_conversion_rate': self.min_conversion_rate,
            },
            'start_date': None,
            'end_date': None,
            'status': 'planned',
        }

        print(f"\n🧪 Discovery Test Plan")
        print(f"   Niche: {niche}")
        print(f"   Market: {target_market}")
        print(f"   Daily Budget: ${self.daily_budget}")
        print(f"   Test Duration: {self.test_duration_days} days")
        print(f"   Total Budget: ${total_budget}")
        print(f"   Estimated Clicks: {int(estimated_clicks)}")
        print(f"\n   Success Criteria:")
        print(f"   - CTR: ≥{self.min_ctr:.1%}")
        print(f"   - CPA: ≤${self.max_cpa}")
        print(f"   - Conversion Rate: ≥{self.min_conversion_rate:.1%}")

        return plan

    def analyze_test_results(
        self,
        impressions: int,
        clicks: int,
        conversions: int,
        total_spend: float
    ) -> Dict:
        """
        Analyze test results and determine if product should scale.

        Args:
            impressions: Ad impressions
            clicks: Ad clicks
            conversions: Landing page conversions
            total_spend: Total amount spent

        Returns:
            Analysis with go/no-go decision
        """
        print(f"\n📊 Analyzing Test Results")

        # Calculate metrics
        ctr = clicks / impressions if impressions > 0 else 0
        conversion_rate = conversions / clicks if clicks > 0 else 0
        cpa = total_spend / conversions if conversions > 0 else float('inf')
        cost_per_click = total_spend / clicks if clicks > 0 else 0

        results = {
            'impressions': impressions,
            'clicks': clicks,
            'conversions': conversions,
            'total_spend': total_spend,
            'metrics': {
                'ctr': ctr,
                'conversion_rate': conversion_rate,
                'cpa': cpa,
                'cost_per_click': cost_per_click,
            },
            'passed_criteria': {
                'sufficient_clicks': clicks >= self.min_clicks,
                'ctr_good': ctr >= self.min_ctr,
                'cpa_good': cpa <= self.max_cpa if conversions > 0 else False,
                'conversion_rate_good': conversion_rate >= self.min_conversion_rate,
            },
            'decision': 'unknown',
            'recommendation': '',
        }

        print(f"   Impressions: {impressions:,}")
        print(f"   Clicks: {clicks}")
        print(f"   Conversions: {conversions}")
        print(f"   Total Spend: ${total_spend:.2f}")
        print(f"\n   Metrics:")
        print(f"   CTR: {ctr:.2%} {'✓' if results['passed_criteria']['ctr_good'] else '✗'}")
        print(f"   Conversion Rate: {conversion_rate:.2%} {'✓' if results['passed_criteria']['conversion_rate_good'] else '✗'}")
        print(f"   CPA: ${cpa:.2f} {'✓' if results['passed_criteria']['cpa_good'] else '✗'}")
        print(f"   Cost/Click: ${cost_per_click:.2f}")

        # Make go/no-go decision
        passed_count = sum(results['passed_criteria'].values())

        if passed_count >= 3:  # Passed 3 out of 4 criteria
            results['decision'] = 'GO'
            results['recommendation'] = "✅ SCALE: Product shows strong potential. Increase budget 3x and continue monitoring."
        elif passed_count == 2:
            results['decision'] = 'OPTIMIZE'
            results['recommendation'] = "⚠️ OPTIMIZE: Some promise but needs improvement. Test different ad creative or adjust landing page."
        else:
            results['decision'] = 'NO-GO'
            results['recommendation'] = "🛑 STOP: Product not performing. Consider different niche or market."

        print(f"\n   Decision: {results['decision']}")
        print(f"   {results['recommendation']}")

        return results

    def calculate_scale_up_budget(
        self,
        current_metrics: Dict,
        scale_multiplier: float = 3
    ) -> Dict:
        """
        Calculate recommended budget after successful test.

        Args:
            current_metrics: Metrics from test
            scale_multiplier: How much to scale budget

        Returns:
            Scale-up recommendation
        """
        cpa = current_metrics['metrics']['cpa']
        conversion_rate = current_metrics['metrics']['conversion_rate']

        # Calculate new budget
        new_daily_budget = self.daily_budget * scale_multiplier

        # Estimate results at scale
        estimated_clicks_per_day = new_daily_budget / current_metrics['metrics']['cost_per_click']
        estimated_conversions_per_day = estimated_clicks_per_day * conversion_rate
        estimated_daily_cost = estimated_conversions_per_day * cpa

        recommendation = {
            'current_daily_budget': self.daily_budget,
            'new_daily_budget': new_daily_budget,
            'scale_multiplier': scale_multiplier,
            'estimated_daily_conversions': estimated_conversions_per_day,
            'estimated_daily_cost': estimated_daily_cost,
            'estimated_daily_profit': 0,  # Calculate based on product price
        }

        print(f"\n📈 Scale-Up Recommendation")
        print(f"   Current Budget: ${self.daily_budget}/day")
        print(f"   New Budget: ${new_daily_budget}/day")
        print(f"   Est. Daily Conversions: {estimated_conversions_per_day:.1f}")
        print(f"   Est. Daily Ad Cost: ${estimated_daily_cost:.2f}")

        return recommendation

    def save_test_data(self, test_plan: Dict, results: Dict, output_path: str):
        """
        Save test data for future reference.

        Args:
            test_plan: Original test plan
            results: Test results
            output_path: Path to save data
        """
        data = {
            'test_plan': test_plan,
            'results': results,
            'timestamp': datetime.now().isoformat(),
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n   💾 Saved test data to: {output_path}")

    def load_test_data(self, input_path: str) -> Dict:
        """Load test data from file."""
        with open(input_path, 'r') as f:
            return json.load(f)

    def generate_test_report(
        self,
        test_plan: Dict,
        results: Dict,
        output_path: str = "test_report.txt"
    ):
        """
        Generate human-readable test report.

        Args:
            test_plan: Test plan data
            results: Test results
            output_path: Path to save report
        """
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║          DISCOVERY TEST REPORT                                 ║
╚════════════════════════════════════════════════════════════════╝

PRODUCT INFO
Niche: {test_plan['niche']}
Market: {test_plan['target_market']}

TEST PARAMETERS
Daily Budget: ${test_plan['daily_budget']}
Test Duration: {test_plan['test_duration_days']} days
Total Budget: ${test_plan['total_budget']}

RESULTS
Impressions: {results['impressions']:,}
Clicks: {results['clicks']}
Conversions: {results['conversions']}
Total Spend: ${results['total_spend']:.2f}

METRICS
CTR: {results['metrics']['ctr']:.2%}
Conversion Rate: {results['metrics']['conversion_rate']:.2%}
CPA: ${results['metrics']['cpa']:.2f}
Cost per Click: ${results['metrics']['cost_per_click']:.2f}

CRITERIA CHECK
✓/✗ Sufficient Clicks: {'✓' if results['passed_criteria']['sufficient_clicks'] else '✗'}
✓/✗ CTR >= {self.min_ctr:.1%}: {'✓' if results['passed_criteria']['ctr_good'] else '✗'}
✓/✗ CPA <= ${self.max_cpa}: {'✓' if results['passed_criteria']['cpa_good'] else '✗'}
✓/✗ Conv Rate >= {self.min_conversion_rate:.1%}: {'✓' if results['passed_criteria']['conversion_rate_good'] else '✗'}

DECISION: {results['decision']}

RECOMMENDATION:
{results['recommendation']}

═══════════════════════════════════════════════════════════════════
Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        with open(output_path, 'w') as f:
            f.write(report)

        print(report)
        print(f"\n   📄 Report saved to: {output_path}")

        return report

    def quick_validation_check(
        self,
        niche: str,
        market: str,
        competitor_count: int,
        estimated_demand: str = "medium"
    ) -> Dict:
        """
        Quick pre-launch validation without spending money.

        Args:
            niche: Product niche
            market: Target market
            competitor_count: Number of competitors found
            estimated_demand: Estimated demand level

        Returns:
            Validation assessment
        """
        print(f"\n⚡ Quick Validation Check")
        print(f"   Niche: {niche}")
        print(f"   Market: {market}")

        # Score the opportunity
        score = 10

        # Competition penalty
        if competitor_count < 5:
            comp_score = 10
        elif competitor_count < 10:
            comp_score = 8
        elif competitor_count < 20:
            comp_score = 6
        else:
            comp_score = 3

        score = comp_score

        # Demand bonus
        demand_scores = {'low': 0, 'medium': 2, 'high': 4}
        score += demand_scores.get(estimated_demand, 2)

        # Make recommendation
        if score >= 8:
            recommendation = "✅ STRONG: High potential. Proceed with discovery test."
        elif score >= 6:
            recommendation = "⚠️ MODERATE: Some potential. Worth testing with low budget."
        else:
            recommendation = "🛑 WEAK: Low potential. Consider different niche/market."

        result = {
            'niche': niche,
            'market': market,
            'competitor_count': competitor_count,
            'estimated_demand': estimated_demand,
            'opportunity_score': score,
            'recommendation': recommendation,
        }

        print(f"   Competitors: {competitor_count}")
        print(f"   Estimated Demand: {estimated_demand}")
        print(f"   Opportunity Score: {score}/10")
        print(f"   {recommendation}")

        return result

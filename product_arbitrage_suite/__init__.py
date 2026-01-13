"""
Product Arbitrage Suite
Automated system for finding, cloning, and launching info products in new markets.

Based on the translation arbitrage strategy:
1. Find proven winners (ads running 14+ days)
2. Clone the funnel structure
3. Create product from YouTube research
4. Translate to underserved markets
5. Launch and profit
"""

from .orchestrator import ProductArbitrageOrchestrator
from .core.market_analyzer import MarketAnalyzer
from .core.ad_monitor import AdMonitor
from .core.funnel_analyzer import FunnelAnalyzer
from .core.content_generator import ContentGenerator
from .core.translator import Translator
from .core.landing_page_builder import LandingPageBuilder

__version__ = "1.0.0"
__all__ = [
    "ProductArbitrageOrchestrator",
    "MarketAnalyzer",
    "AdMonitor",
    "FunnelAnalyzer",
    "ContentGenerator",
    "Translator",
    "LandingPageBuilder",
]

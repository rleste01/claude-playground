"""Translation and localization for different markets."""

from typing import Dict, Optional
from ..utils.ai_helper import AIHelper


class Translator:
    """Translate content and funnels for new markets."""

    # Price adjustments for different markets (based on purchasing power)
    MARKET_CONFIG = {
        'french': {
            'languages': ['french', 'fr'],
            'countries': ['france', 'belgium', 'switzerland', 'canada'],
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.9,
        },
        'german': {
            'languages': ['german', 'de'],
            'countries': ['germany', 'austria', 'switzerland'],
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.95,
        },
        'spanish': {
            'languages': ['spanish', 'es'],
            'countries': ['spain', 'mexico', 'argentina', 'colombia'],
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.7,
        },
        'italian': {
            'languages': ['italian', 'it'],
            'countries': ['italy'],
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.85,
        },
        'portuguese': {
            'languages': ['portuguese', 'pt'],
            'countries': ['portugal', 'brazil'],
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.65,
        }
    }

    def __init__(self, ai_helper: Optional[AIHelper] = None):
        """
        Initialize translator.

        Args:
            ai_helper: AI helper instance
        """
        self.ai_helper = ai_helper or AIHelper()

    def translate_funnel(
        self,
        funnel_blueprint: Dict,
        target_language: str,
        adjust_price: bool = True
    ) -> Dict:
        """
        Translate a complete funnel to a new language.

        Args:
            funnel_blueprint: Funnel blueprint from FunnelAnalyzer
            target_language: Target language
            adjust_price: Whether to adjust price for local market

        Returns:
            Translated funnel blueprint
        """
        print(f"\n🌍 Translating Funnel")
        print(f"   Target Language: {target_language}")

        translated = funnel_blueprint.copy()
        translated['language'] = target_language

        components = funnel_blueprint['components']

        # Translate headline
        print("   Translating headline...")
        translated['components']['headline'] = self.ai_helper.translate_content(
            components['headline'],
            target_language,
            'headline'
        )

        # Translate subheadline
        if components.get('subheadline'):
            print("   Translating subheadline...")
            translated['components']['subheadline'] = self.ai_helper.translate_content(
                components['subheadline'],
                target_language,
                'subheadline'
            )

        # Translate bullets
        print("   Translating bullets...")
        bullets_text = '\n'.join(components['bullets'])
        translated_bullets = self.ai_helper.translate_content(
            bullets_text,
            target_language,
            'bullet points'
        )
        translated['components']['bullets'] = translated_bullets.split('\n')

        # Translate CTA
        print("   Translating CTA...")
        translated['components']['cta'] = self.ai_helper.translate_content(
            components['cta'],
            target_language,
            'call-to-action button'
        )

        # Adjust price
        if adjust_price and components.get('price'):
            new_price = self.adjust_price_for_market(
                components['price'],
                target_language
            )
            translated['components']['price'] = new_price
            print(f"   Adjusted price: {components['price']} → {new_price}")

        print("   ✓ Translation complete")

        return translated

    def translate_product_content(
        self,
        content: str,
        target_language: str
    ) -> str:
        """
        Translate product content to a new language.

        Args:
            content: Original content
            target_language: Target language

        Returns:
            Translated content
        """
        print(f"\n🌍 Translating Product Content")
        print(f"   Target Language: {target_language}")
        print(f"   Content Length: {len(content)} characters")

        # Split content into chunks if too long
        chunk_size = 8000
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

        translated_chunks = []

        for i, chunk in enumerate(chunks, 1):
            print(f"   Translating chunk {i}/{len(chunks)}...")
            translated_chunk = self.ai_helper.translate_content(
                chunk,
                target_language,
                'product content'
            )
            translated_chunks.append(translated_chunk)

        translated_content = '\n\n'.join(translated_chunks)

        print(f"   ✓ Translated to {len(translated_content)} characters")

        return translated_content

    def adjust_price_for_market(
        self,
        original_price: str,
        target_market: str
    ) -> str:
        """
        Adjust price for local market purchasing power.

        Args:
            original_price: Original price (e.g., "$27")
            target_market: Target market/language

        Returns:
            Adjusted price with appropriate currency
        """
        import re

        # Extract numeric price
        price_match = re.search(r'(\d+(?:\.\d{2})?)', original_price)
        if not price_match:
            return original_price

        price_value = float(price_match.group(1))

        # Get market config
        market_config = self.MARKET_CONFIG.get(target_market.lower())

        if not market_config:
            # Default: keep same price
            return original_price

        # Apply multiplier
        adjusted_price = price_value * market_config['price_multiplier']

        # Round to nearest .99 or .00
        adjusted_price = round(adjusted_price)

        # Format with currency
        currency_symbol = market_config['currency_symbol']
        return f"{currency_symbol}{adjusted_price}"

    def get_market_info(self, target_market: str) -> Dict:
        """
        Get information about a target market.

        Args:
            target_market: Target market/language

        Returns:
            Market configuration
        """
        return self.MARKET_CONFIG.get(target_market.lower(), {})

    def polish_translation(
        self,
        translated_content: str,
        target_language: str,
        budget: float = 40
    ) -> str:
        """
        Instructions for polishing translation with human help.

        Args:
            translated_content: AI-translated content
            target_language: Target language
            budget: Budget for human polishing (USD)

        Returns:
            Instructions string
        """
        instructions = f"""
📝 Translation Polishing Required

Your AI-translated content is ready but should be polished by a native speaker.

TASK: Clean up AI translation to sound natural
TARGET LANGUAGE: {target_language}
BUDGET: ${budget}
TIME ESTIMATE: 1-2 hours

WHERE TO FIND HELP:
1. Upwork.com - Search "{target_language} proofreader"
2. Fiverr.com - Search "proofread {target_language}"
3. r/translator on Reddit

INSTRUCTIONS FOR FREELANCER:
"Please review this {target_language} marketing copy and fix any robotic/unnatural phrasing.
Keep the same structure and meaning, just make it sound native.
Focus on making the emotional intensity match the original."

WHAT TO CHECK:
- Sounds natural, not robotic
- Idioms are properly localized
- Persuasive elements maintain impact
- Grammar and spelling are perfect
- Cultural references make sense
"""

        print(instructions)

        return instructions

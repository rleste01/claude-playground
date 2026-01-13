"""Translation and localization for different markets with dialect support."""

from typing import Dict, Optional
from ..utils.ai_helper import AIHelper


class Translator:
    """Translate content and funnels for new markets with proper dialect handling."""

    # Dialect-specific translation guidelines
    DIALECT_GUIDELINES = {
        'brazilian': {
            'language': 'portuguese',
            'full_name': 'Brazilian Portuguese',
            'notes': 'Use Brazilian Portuguese with informal "você" form, Brazilian idioms and local expressions',
            'currency': 'BRL',
            'currency_symbol': 'R$',
            'price_multiplier': 0.4,
            'examples': 'Use "tá" instead of "está", "legal" for "cool", Brazilian vocabulary and slang'
        },
        'european': {
            'language': 'portuguese',
            'full_name': 'European Portuguese',
            'notes': 'Use European Portuguese with more formal register, Portuguese idioms',
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.65,
            'examples': 'Use more formal constructions, "está" instead of "tá", European vocabulary'
        },
        'latin_american': {
            'language': 'spanish',
            'full_name': 'Latin American Spanish',
            'notes': 'Use neutral Latin American Spanish, avoid Spain-specific terms like "vosotros"',
            'currency': 'USD',
            'currency_symbol': '$',
            'price_multiplier': 0.5,
            'examples': 'Use "computadora" not "ordenador", "ustedes" not "vosotros", Latin American vocabulary'
        },
        'european_spanish': {
            'language': 'spanish',
            'full_name': 'European Spanish (Spain)',
            'notes': 'Use European Spanish with vosotros form, Spain-specific terms',
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.7,
            'examples': 'Use "ordenador" not "computadora", vosotros conjugations, Spanish vocabulary'
        },
        'mexican': {
            'language': 'spanish',
            'full_name': 'Mexican Spanish',
            'notes': 'Use Mexican Spanish with local slang and cultural references',
            'currency': 'MXN',
            'currency_symbol': '$',
            'price_multiplier': 0.45,
            'examples': 'Use Mexican vocabulary, local expressions, familiar tone'
        },
        'canadian': {
            'language': 'french',
            'full_name': 'Canadian French (Québécois)',
            'notes': 'Use Québécois expressions and Canadian French vocabulary',
            'currency': 'CAD',
            'currency_symbol': '$',
            'price_multiplier': 0.75,
            'examples': 'Use Québécois terms, Canadian French expressions, local idioms'
        },
        'european_french': {
            'language': 'french',
            'full_name': 'European French',
            'notes': 'Use standard European French without regional variations',
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.9,
            'examples': 'Standard French vocabulary and grammar'
        },
        'swiss': {
            'language': 'german',
            'full_name': 'Swiss German (Standard)',
            'notes': 'Use Standard German with Swiss vocabulary preferences, avoid pure Schwiizerdütsch',
            'currency': 'CHF',
            'currency_symbol': 'CHF',
            'price_multiplier': 1.1,
            'examples': 'Swiss German vocabulary in Standard German, avoid dialect forms'
        },
        'standard': {
            'language': None,  # Will be set based on language
            'full_name': 'Standard',
            'notes': 'Use standard form of the language',
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.85,
            'examples': 'Standard vocabulary and grammar'
        },
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
        dialect: Optional[str] = None,
        adjust_price: bool = True
    ) -> Dict:
        """
        Translate a complete funnel to a new language with dialect support.

        Args:
            funnel_blueprint: Funnel blueprint from FunnelAnalyzer
            target_language: Target language
            dialect: Specific dialect (e.g., 'brazilian', 'latin_american')
            adjust_price: Whether to adjust price for local market

        Returns:
            Translated funnel blueprint
        """
        dialect_info = self._get_dialect_info(target_language, dialect)

        print(f"\n🌍 Translating Funnel")
        print(f"   Target: {dialect_info['full_name']}")

        translated = funnel_blueprint.copy()
        translated['language'] = target_language
        translated['dialect'] = dialect

        components = funnel_blueprint['components']

        # Translate headline
        print("   Translating headline...")
        translated['components']['headline'] = self._translate_with_dialect(
            components['headline'],
            target_language,
            dialect,
            'headline'
        )

        # Translate subheadline
        if components.get('subheadline'):
            print("   Translating subheadline...")
            translated['components']['subheadline'] = self._translate_with_dialect(
                components['subheadline'],
                target_language,
                dialect,
                'subheadline'
            )

        # Translate bullets
        print("   Translating bullets...")
        bullets_text = '\n'.join(components['bullets'])
        translated_bullets = self._translate_with_dialect(
            bullets_text,
            target_language,
            dialect,
            'bullet points'
        )
        translated['components']['bullets'] = [b.strip() for b in translated_bullets.split('\n') if b.strip()]

        # Translate CTA
        print("   Translating CTA...")
        translated['components']['cta'] = self._translate_with_dialect(
            components['cta'],
            target_language,
            dialect,
            'call-to-action button'
        )

        # Adjust price
        if adjust_price and components.get('price'):
            new_price = self.adjust_price_for_dialect(
                components['price'],
                target_language,
                dialect
            )
            translated['components']['price'] = new_price
            print(f"   Adjusted price: {components['price']} → {new_price}")

        print("   ✓ Translation complete")

        return translated

    def translate_product_content(
        self,
        content: str,
        target_language: str,
        dialect: Optional[str] = None
    ) -> str:
        """
        Translate product content to a new language with dialect support.

        Args:
            content: Original content
            target_language: Target language
            dialect: Specific dialect

        Returns:
            Translated content
        """
        dialect_info = self._get_dialect_info(target_language, dialect)

        print(f"\n🌍 Translating Product Content")
        print(f"   Target: {dialect_info['full_name']}")
        print(f"   Content Length: {len(content)} characters")

        # Split content into chunks if too long
        chunk_size = 8000
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

        translated_chunks = []

        for i, chunk in enumerate(chunks, 1):
            print(f"   Translating chunk {i}/{len(chunks)}...")
            translated_chunk = self._translate_with_dialect(
                chunk,
                target_language,
                dialect,
                'product content'
            )
            translated_chunks.append(translated_chunk)

        translated_content = '\n\n'.join(translated_chunks)

        print(f"   ✓ Translated to {len(translated_content)} characters")

        return translated_content

    def _translate_with_dialect(
        self,
        content: str,
        language: str,
        dialect: Optional[str],
        content_type: str
    ) -> str:
        """Translate content with dialect-specific instructions."""
        dialect_info = self._get_dialect_info(language, dialect)

        # Build dialect-aware prompt
        dialect_instruction = ""
        if dialect and dialect != 'standard':
            dialect_instruction = f"""
IMPORTANT DIALECT REQUIREMENTS:
- Target dialect: {dialect_info['full_name']}
- {dialect_info['notes']}
- Examples: {dialect_info['examples']}
- Make it sound authentic to native speakers of this specific dialect
"""

        prompt = f"""You are an expert translator and native copywriter for {dialect_info['full_name']}.

Your job is to adapt this {content_type} into {dialect_info['full_name']} in a way that sounds COMPLETELY NATURAL and PERSUASIVE to native speakers.

{dialect_instruction}

CRITICAL TRANSLATION PHILOSOPHY:
⭐ PRIORITY #1: Sound natural and native - like a native copywriter wrote it from scratch
⭐ PRIORITY #2: Maintain emotional impact and persuasiveness
⭐ PRIORITY #3: Preserve the core meaning and intent

WHEN IN DOUBT: Choose what sounds better and more persuasive to a native speaker over literal word-for-word accuracy.

SPECIFIC REQUIREMENTS:
✓ Use expressions, idioms, and phrasing that native speakers actually use in daily life
✓ Adapt cultural references to be relevant to the target audience
✓ Make it emotionally compelling - native speakers should FEEL the message
✓ Avoid awkward literal translations that technically work but sound robotic
✓ Use the natural word order and sentence structures of the target language
✓ Match the persuasive tone - this is marketing copy that needs to convert
✓ Keep formatting (bullets, numbers, headings, line breaks)

EXAMPLES OF GOOD vs BAD:
❌ BAD: Literal word-for-word translation that sounds mechanical
✅ GOOD: Natural phrasing that a native copywriter would use

Think: "How would a talented native copywriter write this to persuade their own people?"

CONTENT TO TRANSLATE:
{content}

Provide ONLY the translated content that sounds completely natural and persuasive to native {dialect_info['full_name']} speakers.
No explanations, no meta-commentary - just the beautifully adapted copy."""

        return self.ai_helper.generate(prompt, max_tokens=4000)

    def _get_dialect_info(self, language: str, dialect: Optional[str]) -> Dict:
        """Get dialect information."""
        if dialect and dialect in self.DIALECT_GUIDELINES:
            info = self.DIALECT_GUIDELINES[dialect].copy()
            if not info['language']:
                info['language'] = language
            return info

        # Default to standard dialect
        return {
            'language': language,
            'full_name': language.title(),
            'notes': f'Use standard {language}',
            'currency': 'EUR',
            'currency_symbol': '€',
            'price_multiplier': 0.8,
            'examples': 'Standard vocabulary'
        }

    def adjust_price_for_dialect(
        self,
        original_price: str,
        language: str,
        dialect: Optional[str] = None
    ) -> str:
        """
        Adjust price for local market purchasing power with dialect support.

        Args:
            original_price: Original price (e.g., "$27")
            language: Target language
            dialect: Specific dialect

        Returns:
            Adjusted price with appropriate currency
        """
        import re

        # Extract numeric price
        price_match = re.search(r'(\d+(?:\.\d{2})?)', original_price)
        if not price_match:
            return original_price

        price_value = float(price_match.group(1))

        # Get dialect info
        dialect_info = self._get_dialect_info(language, dialect)

        # Apply multiplier
        adjusted_price = price_value * dialect_info['price_multiplier']

        # Round to nearest .99, .97, or .00
        adjusted_price = round(adjusted_price)

        # Format with currency
        currency_symbol = dialect_info['currency_symbol']

        return f"{currency_symbol}{adjusted_price}"

    def get_available_dialects(self, language: Optional[str] = None) -> Dict:
        """
        Get available dialects, optionally filtered by language.

        Args:
            language: Optional language to filter by

        Returns:
            Dictionary of available dialects
        """
        if language:
            return {
                k: v for k, v in self.DIALECT_GUIDELINES.items()
                if v['language'] == language or v['language'] is None
            }

        return self.DIALECT_GUIDELINES

"""Build landing pages from funnel blueprints."""

from typing import Dict, List, Optional
from jinja2 import Template
import os


class LandingPageBuilder:
    """Generate landing pages from funnel blueprints."""

    def __init__(self):
        """Initialize landing page builder."""
        pass

    def build_page(
        self,
        funnel_blueprint: Dict,
        testimonials: Optional[List[str]] = None,
        output_path: str = "landing_page.html"
    ) -> str:
        """
        Build a landing page from funnel blueprint.

        Args:
            funnel_blueprint: Funnel blueprint dictionary
            testimonials: Optional list of testimonial texts
            output_path: Where to save the HTML file

        Returns:
            HTML content
        """
        print(f"\n🏗️  Building Landing Page")
        print(f"   Topic: {funnel_blueprint['topic']}")
        print(f"   Language: {funnel_blueprint['language']}")

        components = funnel_blueprint['components']

        # Generate HTML
        html = self._generate_html(
            headline=components['headline'],
            subheadline=components.get('subheadline', ''),
            bullets=components['bullets'],
            cta=components['cta'],
            price=components['price'],
            testimonials=testimonials or [],
            topic=funnel_blueprint['topic']
        )

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"   ✓ Saved to: {output_path}")

        return html

    def _generate_html(
        self,
        headline: str,
        subheadline: str,
        bullets: List[str],
        cta: str,
        price: str,
        testimonials: List[str],
        topic: str
    ) -> str:
        """Generate HTML from components."""

        template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ topic }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 40px;
        }

        .hero h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            font-weight: 700;
        }

        .hero p {
            font-size: 1.3em;
            opacity: 0.95;
        }

        .content {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .bullets {
            list-style: none;
            margin: 30px 0;
        }

        .bullets li {
            padding: 15px 0;
            padding-left: 30px;
            position: relative;
            font-size: 1.1em;
        }

        .bullets li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
            font-size: 1.2em;
        }

        .price {
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
        }

        .cta {
            display: block;
            width: 100%;
            max-width: 400px;
            margin: 30px auto;
            padding: 20px 40px;
            background: #667eea;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.3em;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        .testimonials {
            margin-top: 50px;
        }

        .testimonial {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }

        .testimonial p {
            font-style: italic;
            color: #555;
        }

        @media (max-width: 600px) {
            .hero h1 {
                font-size: 1.8em;
            }

            .hero p {
                font-size: 1.1em;
            }

            .content {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>{{ headline }}</h1>
            {% if subheadline %}
            <p>{{ subheadline }}</p>
            {% endif %}
        </div>

        <div class="content">
            <h2 style="margin-bottom: 20px; color: #667eea;">What You'll Get:</h2>

            <ul class="bullets">
                {% for bullet in bullets %}
                <li>{{ bullet }}</li>
                {% endfor %}
            </ul>

            <div class="price">{{ price }}</div>

            <a href="#checkout" class="cta">{{ cta }}</a>

            {% if testimonials %}
            <div class="testimonials">
                <h2 style="margin-bottom: 20px; color: #667eea; text-align: center;">What People Are Saying</h2>
                {% for testimonial in testimonials %}
                <div class="testimonial">
                    <p>{{ testimonial }}</p>
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <div style="text-align: center; margin-top: 40px;">
                <a href="#checkout" class="cta">{{ cta }}</a>
            </div>
        </div>

        <div id="checkout" style="background: white; padding: 40px; border-radius: 10px; text-align: center;">
            <h2 style="margin-bottom: 20px;">Checkout</h2>
            <p style="color: #666; margin-bottom: 30px;">Connect your Stripe account or payment processor here</p>

            <!-- Stripe Checkout integration goes here -->
            <div style="padding: 40px; background: #f9f9f9; border-radius: 8px;">
                <p style="color: #999;">
                    💳 Embed Stripe Checkout, Gumroad, or your payment processor
                </p>
            </div>
        </div>
    </div>
</body>
</html>""")

        return template.render(
            topic=topic,
            headline=headline,
            subheadline=subheadline,
            bullets=bullets,
            cta=cta,
            price=price,
            testimonials=testimonials
        )

    def generate_lovable_prompt(self, funnel_blueprint: Dict) -> str:
        """
        Generate a prompt for Lovable.ai to recreate the landing page.

        Args:
            funnel_blueprint: Funnel blueprint

        Returns:
            Lovable prompt
        """
        components = funnel_blueprint['components']

        prompt = f"""Create a landing page with the following structure and copy:

HEADLINE: {components['headline']}

SUBHEADLINE: {components.get('subheadline', '')}

BULLET POINTS:
{chr(10).join(f'- {b}' for b in components['bullets'])}

PRICE: {components['price']}

CTA BUTTON: {components['cta']}

TESTIMONIALS: Include {components.get('num_testimonials', 3)} testimonial sections

DESIGN REQUIREMENTS:
- Modern, clean design
- Hero section with gradient background
- Bullet points with checkmarks
- Large, prominent CTA button
- Testimonial cards with subtle styling
- Embedded checkout section at bottom
- Mobile responsive
- Smooth animations on scroll

COLOR SCHEME: Purple/blue gradient (#667eea to #764ba2)

Keep it simple - pain → solution → buy now. No long copy."""

        print(f"\n🤖 Lovable.ai Prompt:")
        print("=" * 60)
        print(prompt)
        print("=" * 60)

        return prompt

    def add_stripe_checkout(
        self,
        html: str,
        stripe_price_id: str
    ) -> str:
        """
        Add Stripe Checkout integration to HTML.

        Args:
            html: Original HTML
            stripe_price_id: Stripe price ID

        Returns:
            HTML with Stripe integration
        """
        stripe_script = f"""
    <script src="https://js.stripe.com/v3/"></script>
    <script>
        const stripe = Stripe('YOUR_STRIPE_PUBLISHABLE_KEY');

        document.querySelectorAll('.cta').forEach(button => {{
            button.addEventListener('click', async (e) => {{
                e.preventDefault();

                const {{ error }} = await stripe.redirectToCheckout({{
                    lineItems: [{{ price: '{stripe_price_id}', quantity: 1 }}],
                    mode: 'payment',
                    successUrl: window.location.origin + '/success',
                    cancelUrl: window.location.origin + '/cancel',
                }});

                if (error) {{
                    console.error('Error:', error);
                }}
            }});
        }});
    </script>
"""

        # Insert before closing body tag
        html = html.replace('</body>', f'{stripe_script}</body>')

        return html

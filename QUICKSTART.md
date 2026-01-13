# Quick Start Guide

Get your first product arbitrage launched in 6 hours.

## The Process (Real Example)

Let's clone a winning sleep product to the French market.

### Step 1: Find a Winner (15 minutes)

1. Go to [Facebook Ad Library](https://www.facebook.com/ads/library)
2. Search: "sleep" or "fix sleep"
3. Filter: Country = US, Active ads
4. Look at "Started Running" dates
5. Find ads running 14+ days
6. Click through to landing page
7. Save the URL

**What to look for:** Products running 14+ days (profitable), price point $17-97, simple funnels

### Step 2: Research the Topic (30 minutes)

1. Go to YouTube
2. Search: "how to fix sleep naturally"
3. Sort by: View count
4. Find 4 videos with 500k+ views from doctors/experts
5. Copy the URLs

**Example videos:**
- Dr. Andrew Huberman on sleep (2M views)
- Matthew Walker sleep masterclass (800k views)
- Sleep doctor's protocol (600k views)
- Natural sleep fixes (500k views)

### Step 3: Run Automation (15 minutes)

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Run full automation
python run.py full \
  --niche "fix sleep in 7 days" \
  --funnel-url "https://example.com/sleep-landing-page" \
  --youtube-videos \
    "https://youtube.com/watch?v=VIDEO1" \
    "https://youtube.com/watch?v=VIDEO2" \
    "https://youtube.com/watch?v=VIDEO3" \
    "https://youtube.com/watch?v=VIDEO4" \
  --target-market french \
  --output ./output/sleep_french
```

**This generates:**
- ✅ 12-page product guide (English + French)
- ✅ Landing page HTML
- ✅ Funnel blueprint
- ✅ Testimonials in French
- ✅ Lovable.ai prompt

### Step 4: Polish Translation (1-2 hours, $40)

1. Go to Upwork.com
2. Search: "French proofreader"
3. Post job: "Clean up AI-translated marketing copy (1-2 hours)"
4. Budget: $40
5. Share the French product file
6. Ask them to make it sound natural

**What to tell them:**
> "This is marketing copy for a sleep improvement guide. It's already translated but sounds a bit robotic. Please make it sound natural and native. Keep the same structure and persuasive elements. Focus on emotional impact."

### Step 5: Create PDF (15 minutes)

**Option A: Notion**
1. Copy markdown content
2. Paste into new Notion page
3. Format as needed
4. Export as PDF

**Option B: Pandoc**
```bash
pandoc sleep_product_french.md -o sleep_product.pdf
```

### Step 6: Build Landing Page (30 minutes)

**Option A: Use Lovable.ai**
1. Go to [Lovable.ai](https://lovable.ai)
2. Paste the generated prompt from `lovable_prompt.txt`
3. Generate
4. Customize colors/fonts
5. Export code

**Option B: Use Generated HTML**
1. Open `landing_page.html`
2. Customize if needed
3. Deploy to Vercel/Netlify (free)

### Step 7: Set Up Payment (30 minutes)

1. Create Stripe account
2. Create product: "7-Day Sleep Fix" at €27
3. Get Stripe checkout link or price ID
4. Add to landing page
5. Test purchase flow

### Step 8: Launch Ads (1 hour)

**Find Winning Creatives:**
1. Back to Facebook Ad Library
2. Download the ad images/videos you found in Step 1
3. Note the ad copy structure

**Translate Ad Copy:**
```python
from product_arbitrage_suite import Translator

translator = Translator()
french_ad_copy = translator.translate_content(
    "Original English ad copy here",
    target_language="french",
    content_type="Facebook ad"
)
```

**Launch:**
1. Go to Facebook Ads Manager
2. Create campaign: "Traffic" or "Conversions"
3. Target: France, Belgium, Switzerland
4. Budget: €30/day
5. Use translated ad copy + creatives
6. Link to your landing page
7. Launch!

## Expected Timeline

| Step | Time | Cost |
|------|------|------|
| Find winner | 15 min | $0 |
| Research videos | 30 min | $0 |
| Run automation | 15 min | ~$2 (API) |
| Polish translation | 1-2 hrs | $40 |
| Create PDF | 15 min | $0 |
| Build landing page | 30 min | $0 |
| Set up payment | 30 min | $0 |
| Launch ads | 1 hr | €30/day |
| **TOTAL** | **~6 hours** | **~$42 setup + €30/day ads** |

## Expected Results

**Translation arbitrage works consistently because:**
- English markets: Heavily saturated (50-100+ competitors)
- Non-English markets: Significantly less competition (often 5-15 products)
- Proven funnels that already convert in English
- Direct translation into underserved markets

**Typical Economics:**

**Discovery Phase (3 days):**
- Investment: $45 total ($15/day)
- Goal: Validate product-market fit
- Success metrics: 2%+ CTR, <$15 CPA, 1%+ conversion rate

**Scale Phase (if discovery successful):**
- Daily budget: $50-150
- Typical ROI: 300-1000%
- Payback period: 7-14 days
- Monthly profit potential: $3k-15k per product

**Why it works:**
- Same proven structure, 10x less competition
- Proper dialect support increases conversions
- Automated discovery stage minimizes risk
- Quick iteration based on real data

## Scaling Tips

Once your first product is profitable:

### 1. Same Product, More Markets
```bash
# German market
python run.py clone \
  --funnel-url "your-winning-url" \
  --topic "fix sleep in 7 days" \
  --target-market german \
  --output ./output/sleep_german

# Spanish market
python run.py clone \
  --funnel-url "your-winning-url" \
  --topic "fix sleep in 7 days" \
  --target-market spanish \
  --output ./output/sleep_spanish
```

**Additional time:** 2 hours per market
**Additional cost:** $40 translation per market

### 2. Same Funnel, Different Niches

```bash
# Productivity niche
python run.py full \
  --niche "10x your productivity" \
  --funnel-url "your-winning-structure" \
  --youtube-videos [productivity videos] \
  --target-market french \
  --output ./output/productivity_french
```

### 3. Multiple Products, Same Market

Once you prove the market (French works), launch more products:
- Sleep (done)
- Productivity
- Anxiety
- Focus
- Relationships

Each product: ~6 hours setup, €30/day ads

## Common Mistakes to Avoid

❌ **Creating original content** - Copy what works, don't innovate
❌ **Launching in saturated markets** - Target French/German/Spanish first, not English
❌ **Overcomplicating the funnel** - Simple works: problem → solution → buy
❌ **Skipping the polish** - AI translation is good, native speaker makes it great
❌ **Not checking ad longevity** - Only clone ads running 14+ days
❌ **Pricing too high** - Adjust for local purchasing power

## Red Flags

Stop and reassess if:

1. **Can't find winning ads** - Niche might not work, try different one
2. **Ad costs >$15 CPA** - Targeting wrong audience or bad creative
3. **No sales after 100 clicks** - Landing page isn't converting, test different copy
4. **Win rate <30%** - Niche is harder than it looks, pivot

## Success Indicators

Keep scaling when:

✅ CPA < $10
✅ Landing page conversion > 2%
✅ Profit margin > 70%
✅ Low refund rate (<5%)

## Next Steps

1. **Set up your environment:**
   ```bash
   git clone <repo>
   pip install -r requirements.txt
   export ANTHROPIC_API_KEY=your_key
   ```

2. **Do market research:**
   ```bash
   python run.py market --compare --niche sleep
   ```

3. **Find your first winner:**
   - Visit Facebook Ad Library
   - Find ad running 14+ days
   - Note the landing page

4. **Launch:**
   - Follow this guide
   - Start with one niche, one market
   - Track everything
   - Iterate fast

## Support

Questions? Check:
1. Main [README.md](README.md) for detailed docs
2. `examples/` directory for code examples
3. `config.yaml` for configuration options

---

**Remember:** Speed > perfection. Launch in 6 hours, improve based on real data.
# How to Find Winning Digital Products

## The Facebook Ad Library Method (15 minutes)

### Step 1: Access the Ad Library
Go to: https://www.facebook.com/ads/library

### Step 2: Search for Proven Niches

Try these exact searches (sorted by what works best):

**Health/Wellness (HIGHEST SUCCESS RATE)**
- "fix sleep naturally"
- "sleep protocol"
- "anxiety relief"
- "gut health"
- "inflammation"
- "natural remedy"

**Productivity/Self-Improvement**
- "focus better"
- "productivity system"
- "morning routine"
- "time management"

**Relationships**
- "save your marriage"
- "attract women/men"
- "relationship advice"

**Money/Side Hustles**
- "make money online"
- "passive income"
- "side hustle"
- "affiliate marketing"

### Step 3: Filter Settings
- **Country**: United States
- **Ad category**: All ads
- **Status**: Active ads only

### Step 4: Identify Winners (The Magic Formula)

Look for ads with ALL of these signals:

✅ **"Started running on [DATE]"** - Must be 14+ days ago
   - 14-30 days = Profitable and testing
   - 30-90 days = VERY profitable, scaling
   - 90+ days = Print money machine

✅ **Simple offer structure**:
   - "Get the [X-Day Protocol/Guide/System]"
   - Low price point ($17-97)
   - Single product, not complex funnel

✅ **Problem → Solution format**:
   - "Struggling with [problem]?"
   - "Discover the [natural/simple/proven] solution"
   - "Get results in [timeframe]"

✅ **Social proof in ad copy**:
   - Testimonials
   - Results ("10,000+ helped")
   - Authority ("Doctor-approved", "Research-backed")

### Step 5: Click Through to Landing Page

What you want to see:
- Simple one-page site
- Clear headline (problem-focused)
- Bullet points of benefits
- Testimonials (3-5)
- Single CTA button ("Get the Guide")
- Payment via Stripe/Gumroad
- Price clearly visible

**Red flags (skip these):**
- Complex multi-page funnels
- Webinars/calls required
- Physical products
- High-ticket coaching ($500+)
- Too many upsells

---

## 🎯 EXAMPLES OF PERFECT WINNERS

### Example 1: Sleep Protocol ⭐⭐⭐⭐⭐
**Ad Copy Pattern:**
```
Still struggling to fall asleep at night?

Discover the 7-day natural sleep protocol that's helped
10,000+ people sleep like a baby - without pills or supplements.

✓ Fall asleep in under 15 minutes
✓ Wake up refreshed and energized
✓ 100% natural, science-backed

Get instant access to the complete guide for just $27 →
```

**Landing Page:**
- Headline: "The 7-Day Natural Sleep Protocol"
- Subhead: "Fall Asleep Fast, Wake Refreshed - No Pills Required"
- 5-7 bullet points of benefits
- 3-5 testimonials with photos
- "Get Instant Access - $27" button
- FAQ section
- Guarantee (30-day money back)

**Why It Works:**
- Clear problem (can't sleep)
- Specific solution (7-day protocol)
- Low price ($27)
- No physical product
- Instant delivery

**How to Clone This:**
```bash
python run.py full \
  --niche "natural sleep protocol 7 days" \
  --funnel-url "THEIR_LANDING_PAGE_URL" \
  --target-market portuguese \
  --dialect brazilian \
  --output ./output/sleep_brazilian
```

---

### Example 2: Anxiety Relief Guide ⭐⭐⭐⭐
**Ad Copy Pattern:**
```
Feeling anxious and overwhelmed every day?

The 5-minute daily practice that naturally reduces anxiety
- used by 15,000+ people worldwide.

No therapy. No medication. Just simple, proven techniques.

Download the complete guide now - $37 →
```

**Why It Works:**
- Massive market (anxiety = huge)
- Quick solution (5 minutes daily)
- Natural approach
- Price point sweet spot ($37)

---

### Example 3: Productivity System ⭐⭐⭐
**Ad Copy Pattern:**
```
Struggling to focus? Getting nothing done?

Discover the productivity system that helped me 10x my output
- and work just 4 hours per day.

✓ Simple daily routine
✓ No fancy tools needed
✓ Results in 21 days

Get the complete system for $47 →
```

**Why It Works:**
- Universal problem (everyone wants productivity)
- Specific timeframe (21 days)
- Aspirational (4 hours/day)

---

## 🔥 NICHES RANKED BY SUCCESS RATE

### Tier 1 (Highest Success) ⭐⭐⭐⭐⭐
1. **Sleep improvement** - Universal problem, desperate buyers
2. **Anxiety/stress relief** - Huge market, recurring problem
3. **Gut health/digestion** - Growing awareness, clear pain point

### Tier 2 (Very Good) ⭐⭐⭐⭐
4. **Productivity/focus** - Everyone wants it
5. **Natural remedies** (inflammation, pain, etc.)
6. **Weight loss** (harder but HUGE market)

### Tier 3 (Good) ⭐⭐⭐
7. **Relationship advice** - Emotional buyers
8. **Side hustles/money** - Saturated but big
9. **Habit building** - Growing niche

### Avoid (Too Hard for Beginners) ❌
- B2B/business tools
- Technical skills (coding, design)
- Highly regulated (medical advice, legal)
- Physical fitness (needs video demos)

---

## 💰 PRICING SWEET SPOTS

**By Market (Auto-adjusted in config.yaml):**

| Original (EN) | Brazilian (BR) | French (FR) | Spanish (MX) |
|---------------|----------------|-------------|--------------|
| $27           | R$97 (~$20)    | €24 (~$27)  | $399 MXN (~$21) |
| $37           | R$127 (~$26)   | €34 (~$38)  | $549 MXN (~$28) |
| $47           | R$157 (~$32)   | €42 (~$47)  | $699 MXN (~$36) |

**Best Price Range:**
- Entry products: $27-37
- Core products: $37-57
- Premium: $67-97

---

## ✅ YOUR ACTION CHECKLIST

### Today (30 minutes):
- [ ] Go to Facebook Ad Library
- [ ] Search "fix sleep naturally"
- [ ] Find 3 ads running 14+ days
- [ ] Click through to landing pages
- [ ] Pick the simplest one
- [ ] Save the URL

### This Week:
- [ ] Get Anthropic API key
- [ ] Run automation on chosen winner
- [ ] Review generated content
- [ ] Polish translation ($40)
- [ ] Deploy landing page
- [ ] Launch discovery ads ($45)

### Decision Point (After 3 days):
- [ ] Check metrics (CTR, CPA, conversions)
- [ ] If successful: Scale budget
- [ ] If not: Try different niche

---

## 🎬 QUICK START SCRIPT

Once you find a winner, use this exact command:

```bash
# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Clone the winner
python run.py full \
  --niche "YOUR_NICHE_FROM_AD" \
  --funnel-url "LANDING_PAGE_YOU_FOUND" \
  --target-market portuguese \
  --dialect brazilian \
  --output ./output/first_product

# Wait 2-3 minutes for automation to complete

# You'll get:
# ✓ Product guide (Portuguese)
# ✓ Landing page HTML
# ✓ Ad copy suggestions
# ✓ Testimonials
```

---

## 💡 PRO TIPS

**Finding Winners Faster:**
1. Sort by "Recently Active" in Ad Library
2. Look for ads with lots of comments/reactions
3. Check if multiple similar ads exist (= working niche)
4. Use Google to search "[niche] guide PDF" - see what exists

**Red Flags to Skip:**
- Ads running <14 days (not validated yet)
- Complex sales funnels
- Physical products
- High-ticket ($500+)
- Requires video/calls
- Supplement/physical product upsells

**Green Flags (Clone These!):**
- Simple one-page site
- Clear PDF/guide delivery
- Price $17-97
- Natural/simple solution
- Specific timeframe (7 days, 21 days, etc.)
- Problem everyone relates to

---

## 🚀 NEXT STEPS

1. **Right now**: Open Facebook Ad Library in new tab
2. **Search**: "fix sleep naturally"
3. **Find**: One ad running 20+ days
4. **Report back**: Share the URL and we'll analyze it together

Ready to find your first winner? 🎯

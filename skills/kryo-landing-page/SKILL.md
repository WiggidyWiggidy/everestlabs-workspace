# SKILL: kryo-landing-page
Write KRYO Shopify landing page copy for split testing.

## Before Writing
1. Read `/home/node/.openclaw/workspace/KRYO.md` — full product + brand context
2. Read `docs/customer-avatar-dubai.md` from GitHub — who we're writing for
3. Read `docs/brand-voice.md` — tone rules
4. Read `data/feedback.json` — lessons from past approved/rejected pages
5. Note which angle the paired Meta ad is running — landing page must match

## Page Structure (Standard)

### 1. HERO
- **Headline:** Big outcome claim. 6–10 words max.
- **Subheadline:** The mechanism or the proof. 1 sentence.
- **CTA button:** Above the fold. "Get KRYO" / "Shop Now"
- **Hero image/video:** Show the product in use. Cold steam. Sharp person. Dubai context.

### 2. PROBLEM
- Name the Dubai-specific pain. Warm tap water. No space. Caffeine dependency.
- 2–3 short paragraphs or bullet points.
- Don't be preachy. Just make them feel the problem.

### 3. SOLUTION
- Introduce KRYO as the logical answer.
- Key specs framed as outcomes (NOT feature lists):
  - 1°C water → "Cold enough to actually work"
  - 14L reservoir → "Always ready. No ice. No waiting."
  - 30 seconds → "That's all your nervous system needs."
  - Apartment-friendly → "No outdoor space required."

### 4. SCIENCE / CREDIBILITY
- 2–3 science points (dopamine spike, cortisol regulation, CNS activation)
- Reference: Huberman, Rhonda Patrick, clinical cold exposure studies
- Optional: celebrity social proof (Joe Rogan, Chris Hemsworth on cold exposure)

### 5. SOCIAL PROOF
- Testimonials from high-performers (write placeholder versions for testing)
- Format: Quote → Name → Title/Context
- Focus on outcomes: "I stopped needing coffee by day 3"

### 6. OFFER BLOCK
- Price: $1,000 USD (or AED equivalent)
- What's included: Unit + pump + showerhead + installation guide
- Optional: Payment plan, guarantee, limited availability
- CTA: Final button — "Get KRYO" — bold, direct

### 7. FAQ (optional)
- Does it work with any shower? Yes.
- How cold does it get? 1°C — colder than any tap.
- Will it fit my apartment bathroom? Yes — dimensions X × Y × Z
- Is it safe? Yes — temperature regulated, medical-grade components.

## A/B Test Variables
Each variant should change ONE thing:
- Variant A vs B: Different hero headline (productivity angle vs caffeine angle)
- Variant A vs B: Different offer (price displayed vs payment plan lead)
- Variant A vs B: Problem section length (short vs detailed)
- Variant A vs B: Social proof position (above vs below science section)

## Output Format
```
VARIANT: [A / B]
PAIRED AD ANGLE: [angle name]

HERO HEADLINE: 
HERO SUBHEADLINE:
CTA:

PROBLEM SECTION:
[copy]

SOLUTION SECTION:
[copy]

SCIENCE SECTION:
[copy]

SOCIAL PROOF (3 testimonials):
[copy]

OFFER BLOCK:
[copy]

FAQ:
[copy]
```

## Feedback Loop
After Happy reviews:
```
python3 /home/node/.openclaw/workspace/github_push.py log_feedback '{
  "type": "landing_page",
  "draft": "<section or variant>",
  "feedback": "<Happy feedback>",
  "approved": true/false,
  "lesson": "<what to change next time>"
}'
```

## When Assets Arrive
- Study Happy's existing landing pages for structure and offer that works
- Study Eight Sleep landing pages for tone and section order
- Update this skill with proven section templates
- Tag each approved section as a reusable block

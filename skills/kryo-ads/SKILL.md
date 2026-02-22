# SKILL: kryo-ads
Write KRYO Meta ad copy (Facebook/Instagram) for the Dubai launch.

## Before Writing
1. Read `/home/node/.openclaw/workspace/KRYO.md` — product, avatar, brand voice
2. Read `data/feedback.json` from GitHub for lessons from past approved/rejected copy
3. Check which angles are already running (avoid duplicating live experiments)

## Output Format
Always produce in this structure:

```
ANGLE: [angle name]
VARIANT: [A/B/C]

PRIMARY TEXT:
[2–4 lines max. Hook → proof/insight → CTA]

HEADLINE:
[5–8 words. Punchy. Outcome or curiosity.]

DESCRIPTION:
[1 line. Optional. Reinforces headline.]

CTA BUTTON: [Shop Now / Learn More / Get KRYO]
```

Produce 5 angles × 3 variants = 15 pieces minimum per batch.

## The 5 Core Angles
1. **Productivity** — "Win back 30 minutes every morning"
2. **Caffeine replacement** — "The coffee you don't need"
3. **Dubai problem** — "Dubai tap water is 35°C. KRYO is 1°C."
4. **Identity/status** — "Built for people who take mornings seriously"
5. **Science** — Cold exposure → dopamine spike → CNS activation

## Copy Rules (from Brand Voice)
- Outcome first, feature second
- Short sentences. Declarative. Punchy.
- No woo language. Science or ROI only.
- Never use: relax, pamper, affordable, simply, amazing, incredible
- Always use: sharp, awake, cold, 1°C, 30 seconds, performance, edge

## Hook Formulas That Work
- **Problem hook:** "Dubai does not do cold showers." 
- **Stat hook:** "30 seconds. That is all it takes."
- **Identity hook:** "Some people optimise their diet, their sleep, their gym. Then ruin it with coffee."
- **Question hook:** "What if your morning shower actually woke you up?"
- **Contrast hook:** "Your tap: 35°C. KRYO: 1°C. Your morning: changed."

## Feedback Loop
After Happy reviews, log feedback immediately:
```
python3 /home/node/.openclaw/workspace/github_push.py log_feedback '{
  "type": "ad_copy",
  "draft": "<copy variant>",
  "feedback": "<Happy feedback>",
  "approved": true/false,
  "lesson": "<what to do differently next time>"
}'
```

## When Assets Arrive (Tomorrow)
- Incorporate Happy's winning copy patterns
- Match tone/structure of what has already converted
- Layer Eight Sleep examples as style reference — adapt, don't copy
- Update this SKILL.md with new lessons after first review session

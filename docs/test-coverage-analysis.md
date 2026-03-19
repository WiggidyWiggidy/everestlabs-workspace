# Test Coverage Analysis — KRYO Workspace

**Date:** 2026-03-19
**Scope:** Full repository audit of `everestlabs-workspace`

---

## Current State: No Automated Tests

This repository is a **content operations system** (brand docs, AI skill definitions, marketing copy, structured JSON data), not a traditional software codebase. There are currently:

- 0 test files
- 0 test frameworks
- 0 CI/CD pipelines
- 0 schema validation

Everything relies on manual human review (Happy approves/rejects drafts).

---

## Recommended Testing Areas

### 1. JSON Schema Validation (High Priority)

**Problem:** The 5 data files (`feedback.json`, `experiments.json`, `ideas.json`, `marketing.json`, `tokens.json`) have no enforced schemas. Any malformed write — from a script, a skill, or a manual edit — could silently break the feedback loop or dashboard.

**What to test:**
- `tokens.json`: Every session object must have `id`, `date`, `model`, `inputTokens`, `outputTokens`, `totalTokens`, and either `cost` or `estimatedCost` (currently inconsistent — some entries use `cost`, others use `estimatedCost` with a string instead of a number)
- `feedback.json`: Every entry must have `id`, `date`, `type` (enum: `test`, `ad_copy`, `landing_page`), `draft`, `feedback`, `approved` (boolean), `lesson`
- `ideas.json`: Every entry must have `id`, `text`, `tag`, `source`, `date`, `promoted` (boolean)
- `experiments.json`: Define the expected schema before data starts flowing

**How:** Add JSON Schema files (`schemas/`) and a simple validation script (Node.js or Python) that checks each data file against its schema.

---

### 2. Brand Voice Compliance (High Priority)

**Problem:** The brand voice doc (`docs/brand-voice.md`) defines explicit word rules — words to always use and words to never use — but there's no automated check that generated copy follows these rules.

**What to test:**
- **Banned words:** Scan all files in `copy/` for: *relax, pamper, affordable, simply, amazing, incredible*
- **Required tone markers:** Verify presence of at least some of: *sharp, awake, cold, 1°C, 30 seconds, performance, edge*
- **Sentence length:** Flag any sentence over 20 words (brand voice says "short sentences, declarative, punchy")

**How:** A linting script that runs against `copy/**/*.md` and reports violations. Could be a pre-commit hook or a CI check.

---

### 3. Ad Copy Structure Validation (Medium Priority)

**Problem:** The ad skill (`skills/kryo-ads/SKILL.md`) requires a specific output format (ANGLE, VARIANT, PRIMARY TEXT, HEADLINE, DESCRIPTION, CTA BUTTON) and a minimum of 5 angles x 3 variants = 15 pieces per batch. There's no automated check that generated batches meet this spec.

**What to test:**
- Every file in `copy/ads/` parses into exactly 15 structured ad units
- Each ad has all required fields (ANGLE, VARIANT, PRIMARY TEXT, HEADLINE, CTA BUTTON)
- All 5 core angles are represented (Productivity, Caffeine Replacement, Dubai Problem, Identity/Status, Science)
- Each angle has exactly 3 variants (A, B, C)
- Headlines are 5-8 words
- Primary text is 2-4 lines

**How:** A parser script that reads batch files and validates structure + counts.

---

### 4. Landing Page Copy Structure Validation (Medium Priority)

**Problem:** Same as above but for landing pages. The skill defines 7 required sections (Hero, Problem, Solution, Science, Social Proof, Offer, FAQ) and A/B test variables.

**What to test:**
- Every landing page variant has all 7 sections
- Each variant is paired with a named ad angle
- A/B variants change exactly ONE variable (not multiple)
- Hero headline is 6-10 words

---

### 5. Data Integrity & Consistency (Medium Priority)

**Problem:** `tokens.json` already shows inconsistencies:
- Some entries have `cost` (number), others have `estimatedCost` (string) — lines 63 vs 68
- Some entries are missing the `id` field (last entry)
- Some entries are missing `task_type` (entries on lines 42-73)

**What to test:**
- All fields use consistent naming (`cost` vs `estimatedCost` — pick one)
- All numeric fields are actually numbers (not strings like `"0.22"`)
- All entries have an `id`
- No duplicate IDs across any data file

**How:** Validation script that loads each JSON file and checks field types + uniqueness.

---

### 6. Cross-Reference Integrity (Low Priority)

**Problem:** Skills reference external file paths (`/home/node/.openclaw/workspace/KRYO.md`, `github_push.py`) that may not exist in all environments.

**What to test:**
- All file paths referenced in SKILL.md files actually resolve
- The `github_push.py` script referenced in feedback loops exists and is callable
- Feedback types logged in `feedback.json` match the `type` enum expected by skills

---

### 7. Experiment Tracking Readiness (Low Priority)

**Problem:** `experiments.json` is empty. When A/B test data starts flowing in, there's no schema or validation in place.

**What to test:**
- Define and document the experiment schema before first data entry
- Validate that experiment entries reference valid ad angles / landing page variants
- Ensure experiment IDs don't collide with other data files

---

## Suggested Implementation Order

| Priority | Area | Effort | Impact |
|----------|------|--------|--------|
| 1 | JSON Schema Validation | Low | High — prevents silent data corruption |
| 2 | Brand Voice Compliance Linter | Low | High — catches off-brand copy before review |
| 3 | Ad Copy Structure Validation | Medium | Medium — ensures batch completeness |
| 4 | Data Integrity Fixes | Low | Medium — fix existing inconsistencies in tokens.json |
| 5 | Landing Page Validation | Medium | Medium — mirrors ad copy validation |
| 6 | Cross-Reference Checks | Low | Low — environment-specific paths |
| 7 | Experiment Schema Definition | Low | Low — preparation for future data |

---

## Quick Wins (Can Do Now)

1. **Fix `tokens.json` inconsistencies** — normalize `cost`/`estimatedCost`, ensure all values are numbers, add missing `id` fields
2. **Add a `schemas/` directory** with JSON Schema definitions for each data file
3. **Write a 20-line brand voice linter** that greps `copy/` for banned words
4. **Add a `.github/workflows/validate.yml`** that runs schema + linting checks on every push

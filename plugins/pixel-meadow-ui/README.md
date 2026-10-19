# pixel-meadow-ui

A Claude design skill for warm, premium landing pages: 16-bit pixel-art nature scenes inside rounded inset frames, frosted-glass pill navigation, DM Sans display type with one Instrument Serif italic accent, butter-yellow and white pill buttons, paper-white sections in deep green ink, pastel cards, and slow blur-in motion.

The pixel art is generated in code (`pixel-scene.js`, zero dependencies), so pages ship without any image files.

## What it gives Claude

- **Two working templates**: a one-screen "cinematic" waitlist and a full "paper" product landing page (hero, proof strip, pastel step cards, tabs with a product mock, an art-card feature, pricing calculator, FAQ, closing band, footer)
- **Procedural scenes**: `meadow` (calm green hills), `bloom` (giant sunflowers), `dusk` (setting sun, fireflies, for letters and about pages), `highland` (golden hour, table mountains, acacias, round huts), plus pixel bees and butterflies, pollen motes and mouse parallax
- **Design tokens and a component catalog**: exact type scale, colors, radii, spacing and motion curves
- **Voice rules**: two-short-sentence headlines, kind microcopy, no hype words

It reproduces the design language only, never another site's name, logo, copy or artwork.

## Install

**Claude Code (plugin)**

```
/plugin marketplace add lijnati/saas-brand-namer
/plugin install pixel-meadow-ui@lijnati-skills
```

**Claude Code (manual)**

```bash
git clone https://github.com/lijnati/saas-brand-namer.git /tmp/lijnati-skills
cp -r /tmp/lijnati-skills/plugins/pixel-meadow-ui/skills/pixel-meadow-ui ~/.claude/skills/
```

## Usage

Ask for a page in plain words. It triggers on requests like:

- "build a landing page for my MCP server, cozy pixel-art style"
- "coming soon page for my wellbeing app, calm, like millow.space"
- "write our founder letter as a long-read page with a dusk scene"

## Layout

```
.claude-plugin/plugin.json
skills/pixel-meadow-ui/
  SKILL.md                  workflow, non-negotiables, voice
  references/tokens.md      type, color, shape, motion specs
  references/components.md  section patterns and scene API
  assets/pixel-scene.js     procedural pixel-art generator
  assets/template-*.html    working templates
```

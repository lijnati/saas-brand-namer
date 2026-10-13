---
name: saas-brand-namer
description: Generate distinctive one-word brand names for SaaS products, startups, dev tools, apps, agents, and side projects. Use this whenever the user asks to name (or rename) a product, company, startup, app, tool, protocol, feature, or project, wants name ideas or alternatives, says their current name is generic, taken, or sounds AI-generated, or wants something that "sounds like Linear, Vercel, or Stripe". Outputs single-word names only and rejects the glued two-word pattern (ScopePilot, BriefBridge, VendorVault) plus the one-word AI cliches (Nexus, Lumina, Aegis).
---

# One-Word SaaS Brand Namer

Produce a shortlist of brand names that are **one word**, ownable, easy to say, and do not sound like an LLM made them up.

## Why this skill exists

Ask any model to name a SaaS and it glues a domain noun to a metaphor noun: ScopePilot, BriefBridge, VendorVault, CostGuard, DataForge. That pattern is the naming equivalent of stock photography. It is descriptive instead of ownable, the .com is gone, it is weak for trademarks, and a thousand products already sound exactly like it. The fallback single-word version is just as tired: Nexus, Lumina, Vertex, Aegis, Pulse.

The brands people remember are one word with a little tension between the word and the product: Linear, Stripe, Notion, Vercel, Figma, Ramp, Loom, Clerk, Plaid, Gusto, Arc, Zed, Granola. Aim there.

## What counts as one word

- A single token. No spaces, hyphens, dots, digits, or CamelCase capitals in the middle. "ScopePilot" and "Scopepilot" are the same mistake.
- Not two common words glued together (Costwise, Sunpath, Dropbox shape). A word that already exists as one dictionary word is fine even if smaller words hide inside it (Carpet, Notion).
- Not a word with a SaaS suffix stuck on: -ly, -ify, -io, -ai, -hub, -labs, -hq, -base, -stack, -flow, -kit, -bot, -ops, -sync, -wise, -verse, -mind, -gpt. "Taskly" and "Budgetio" are the compound pattern wearing a disguise. Coined words that merely end in those letters (Twilio, Attio) are fine because there is no real word underneath.
- No vowel-dropped spellings (Flickr, Tumblr). That trope peaked in 2008.
- 3 to 9 letters is the sweet spot. Up to 12 only with a strong reason.

## The second kind of slop

One word is not enough on its own. Steer away from the names models reach for by reflex: cosmic grandeur (Nexus, Nova, Zenith, Apex, Vertex, Horizon, Orbit), pseudo-science (Quantum, Synapse, Cortex, Helix, Flux, Axiom), energy cliches (Pulse, Spark, Elevate, Velocity, Surge), vibe words (Aura, Echo, Prism, Lumina, Onyx), guardian nouns (Sentinel, Beacon, Forge, Vault, Pilot, Aegis, Atlas, Compass), and default gods (Athena, Hermes, Apollo, Oracle, Phoenix). Also avoid Omni-, Hyper-, Meta-, Neo-, Smart- prefixes.

The full list lives in `assets/slop_words.txt` and the lint script enforces it. If a name feels like it would appear in a list of "50 futuristic startup names", it belongs there too.

## Process

### 1. Understand the product

Pull out, from whatever the user gave you:
- **The job**: what the product does, as one verb (reconcile, watch, schedule, ship).
- **The buyer**: who pays (indie devs, finance teams, SMEs, creators).
- **The feel**: two or three adjectives (fast, calm, sharp, trustworthy, playful, premium).
- **The market**: global or regional, and which languages matter for pronunciation and bad-meaning checks.
- **Any constraints**: names they already rejected, letters or sounds they like, names of competitors.

If the request is thin, infer and state your read in one line rather than interrogating the user. Ask only when you cannot tell what the product does.

### 2. Gather raw material

Write 20 to 30 concept seeds before naming anything: the core action, the outcome, the object the user touches, the physical mechanism behind it, how the user feels once the problem is gone. Then go sideways into adjacent fields: navigation, textiles, geology, weather, music, cooking, typography, old trades, tools a craftsperson would hold.

The good names live in the second and third associations. The first association for "AI cost monitoring" is Guard, Watch, Budget, Meter, and so is everyone else's. Keep going until the seeds surprise you.

### 3. Generate wide

Produce 40+ candidates spread across at least five of these strategies, so the pool is not 40 Latin roots:

| Strategy | How it works | Real examples |
|---|---|---|
| Repurposed real word | Everyday word with an unexpected but defensible link to the product | Linear, Stripe, Notion, Slack, Ramp, Loom, Clerk, Plaid |
| Coined word | Invented from sound, not meaning; must be easy to say and spell | Vercel, Zapier, Kodak, Hulu, Attio |
| Clipped or fused root | Fragments of meaning fused into one new word that does not read as two words | Figma, Twilio, Vimeo |
| Foreign or archaic word | A word from another language or old English, chosen for meaning and easy pronunciation | Ubuntu, Gusto, Asana, Volvo |
| Proper noun | Surname, given name, place, ship or historical figure | Tesla, Oscar, Patagonia |
| Unexpected concrete noun | A tangible thing with no surface link, which makes it memorable | Apple, Granola, Arc, Pebble |
| Short syllable | Two to four letters of pure sound | Zed, Arc, Hex, Ox |

For foreign words, prefer languages relevant to the founder or market when the user signals it, and only use words whose meaning you are confident about.

### 4. Filter hard

Save the candidate pool to a file and run the linter:

```bash
python <skill-dir>/scripts/lint_names.py --file candidates.txt
```

It FAILs non-single-tokens, glued compounds, stuck-on suffixes, slop-list words and unpronounceable strings, and WARNs on length, awkward clusters, vowel-dropping and compound-looking dictionary words. Drop every FAIL. Keep a WARN only if you can say why it is worth it.

Then apply the judgment tests the script cannot:
- **Radio test**: hear it once, could you type it correctly? (Kwyk fails. Ramp passes.)
- **Sentence test**: "We moved our billing to ___." "I'll ___ it to you." Does it sound like a company?
- **Descriptive test**: a name that just describes the product ("Invoice" for invoicing) is unownable. Suggestive beats descriptive.
- **Meaning check**: look for bad meanings or slang in English and the main languages of the user's market. If you are unsure, say so instead of guessing.
- **Collision check**: if a famous company already uses it in the same category, drop it. If it is known in a different category, keep it but flag it.

### 5. Shortlist

Pick 10 to 12 survivors, ranked. Use no more than three from any single strategy so the user sees real range.

### 6. Verify only what you can

If web search is available, check the top 3 to 5 for an existing SaaS with the same name in the same space and report what you found. Never state that a domain or trademark is available unless you actually checked. Real words will not have a free .com, and that is normal: suggest workable patterns (`name.dev`, `name.so`, `name.app`, `getname.com`, `usename.com`) and recommend a trademark search (USPTO, WIPO Global Brand Database, or the local registry) before the user commits.

## Output format

Use this structure:

```
Naming for: <product in one line> | Feel: <2-3 adjectives>

## Top picks

**1. Name** (pronunciation if not obvious) · <strategy>
Why it fits: <one or two sentences linking the word to the product or feeling>
Watch out: <the main risk, or "nothing obvious">
Domains to try: name.dev, getname.com, name.so

**2. ...**
**3. ...**

## More options
- **Name**: one-line reason
- ... (7 to 9 more)

Skipped on purpose: <3-4 names this product would usually get, e.g. CostGuard, SpendPilot, Budgetly>
```

Close with a single next step, such as "Want 10 more in the direction of #2?" or "Want me to check conflicts for the top three?"

Keep rationales concrete. "Evokes trust and innovation" says nothing. "A ledger reconciles two columns; so does the product" says something.

## Iterating

- **"More like #3"**: generate 10 more with the same strategy, length, and sound profile (hard consonants, open vowels, and so on).
- **"None of these"**: do not just reroll. Offer three deliberately different directions (for example: plain real word, coined and soft, short and sharp) with two names each and ask which way to go.
- **The user suggests a name**: run it through the linter and the judgment tests and give an honest verdict. If it is a glued compound or a slop word, say so and offer one-word alternatives with the same intent.

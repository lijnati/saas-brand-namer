# saas-brand-namer

A Claude skill that generates one-word brand names for SaaS products, dev tools and startups, and refuses to produce the AI naming slop everyone recognizes.

No more `ScopePilot`, `BriefBridge`, `VendorVault`, `CostGuard`. No more `Nexus`, `Lumina`, `Vertex` either. Names in the spirit of Linear, Stripe, Notion, Vercel, Figma, Ramp.

## What it does

- Generates **single-word names only**: no CamelCase, no glued compounds, no `-ly` / `-ify` / `-io` / `-hub` suffix tricks
- Blocks single-word cliches with a curated slop list (`skills/saas-brand-namer/assets/slop_words.txt`)
- Generates 40+ candidates across seven strategies (repurposed words, coined words, fused roots, foreign words, proper nouns, unexpected objects, short syllables), then filters to a ranked shortlist
- Explains each pick: why it fits, the main risk, and domain patterns to try
- Never claims a domain or trademark is available unless it actually checked
- Gives an honest verdict when you propose your own name

## Example

> **Prompt:** We're calling our AI API cost monitoring tool TokenGuard. Is that good?
>
> **Verdict:** not recommended. Glued CamelCase compound, purely descriptive, and "Guard" is in hundreds of tool names.
>
> **Top picks:** Weir (a low dam that controls flow instead of blocking it), Governor, Ballast

More sample runs live in [`examples/test-outputs.md`](examples/test-outputs.md).

## Install

**Claude Code (plugin, recommended)**

Inside Claude Code, run:

```
/plugin install saas-brand-namer --marketplace lijnati/saas-brand-namer
```

On Claude Code versions before 2.1.275, add the marketplace first, then install:

```
/plugin marketplace add lijnati/saas-brand-namer
/plugin install saas-brand-namer@lijnati-skills
```

Updates arrive through `/plugin marketplace update lijnati-skills`.

**Claude Code (manual)**

```bash
git clone https://github.com/lijnati/saas-brand-namer.git /tmp/saas-brand-namer
cp -r /tmp/saas-brand-namer/skills/saas-brand-namer ~/.claude/skills/
```

**Claude apps**

Build the package with `./build.sh`, then upload `dist/saas-brand-namer.skill` in Claude's skills settings.

## Usage

Just ask Claude to name something. The skill triggers on requests like:

- "name my waitlist SaaS for indie hackers"
- "I need a brand name that feels like Linear"
- "our product name sounds AI-generated, give me alternatives"

## The linter

The skill ships a standalone linter you can run on any list of names:

```bash
python skills/saas-brand-namer/scripts/lint_names.py Vercel ScopePilot Lumina Taskly
```

```
PASS  Vercel
FAIL  ScopePilot  CamelCase internal capital (reads as two words); glued compound: 'scope' + 'pilot'; ...
FAIL  Lumina      overused AI/tech cliche (slop list)
FAIL  Taskly      word + stuck-on suffix '-ly'; ...
```

Options: `--file candidates.txt` to read one name per line, `--json` for machine-readable output. Python 3.8+, no dependencies.

Compound detection uses `skills/saas-brand-namer/assets/words.txt`, the 38k most frequent English words, derived from [wordfreq](https://github.com/rspeer/wordfreq) data (CC BY-SA 4.0, so that one file keeps its original license).

## Customize

- **Ban more words:** add them to `skills/saas-brand-namer/assets/slop_words.txt`, one per line
- **Allow a word:** delete its line from the same file
- **Change the rules:** suffix and prefix lists are at the top of `skills/saas-brand-namer/scripts/lint_names.py`

## Repo layout

```
.claude-plugin/
  plugin.json         plugin manifest
  marketplace.json    lets this repo act as its own marketplace (lijnati-skills)
skills/saas-brand-namer/
  SKILL.md            the skill
  scripts/            name linter
  assets/             slop list and word list
tests/                linter tests
examples/             sample runs
```

## Development

```bash
python -m unittest discover tests      # run the linter tests
claude plugin validate .               # validate plugin and marketplace manifests
./build.sh                             # package dist/saas-brand-namer.skill
```

## License

MIT for the skill and code. `skills/saas-brand-namer/assets/words.txt` is derived from wordfreq data and is licensed CC BY-SA 4.0.

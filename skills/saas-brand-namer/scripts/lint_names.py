#!/usr/bin/env python3
"""Lint brand name candidates against the one-word rules.

Usage:
    python lint_names.py Vercel ScopePilot Lumina Taskly
    python lint_names.py --file candidates.txt
    python lint_names.py --json Vercel Ramp          # machine-readable output

Each name gets PASS, WARN or FAIL with reasons.
FAIL = breaks a hard rule (not one word, glued compound, slop word, stuck-on suffix).
WARN = worth a second look (long, hard to say, vowel-dropped spelling, slop prefix).
The script only catches mechanical problems. Taste, meaning and fit are still on you.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"

# Fragments people glue onto a word to make a "one-word" SaaS name. Only checked
# when the whole name is NOT itself a dictionary word (so "Rely" or "Fly" are fine).
BANNED_SUFFIXES = [
    "ly", "ify", "io", "hub", "ai", "labs", "lab", "hq", "base", "stack", "flow",
    "app", "kit", "bot", "iq", "ops", "sync", "wise", "genie", "mind", "verse",
    "pilot", "forge", "vault", "bridge", "nest", "hive", "scope", "spark",
    "pulse", "sense", "loop", "craft", "works", "desk", "zen", "gpt", "able",
]
BANNED_PREFIXES = ["omni", "hyper", "meta", "neo", "quantum", "nexu", "smart", "auto", "ai"]


def load_words():
    path = ASSETS / "words.txt"
    if not path.exists():
        return set(), set()
    words = [w.strip() for w in path.read_text().splitlines() if w.strip()]
    full = set(words)
    # Parts of a compound must be fairly common words, so obscure splits
    # like "ver" + "cel" don't trigger a false alarm.
    core = set(w for w in words[:10000] if len(w) >= 3)
    return full, core


def load_slop():
    path = ASSETS / "slop_words.txt"
    if not path.exists():
        return set()
    return {
        line.strip().lower()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }


WORDS, CORE = load_words()
SLOP = load_slop()


# Short fragments that are common as words in frequency lists but are really
# prefixes, so "resend" is not read as "res" + "end".
AFFIX_LIKE = {"res", "pre", "pro", "con", "com", "dis", "per", "sub", "ver", "tri", "uni", "bio", "eco"}


def compound_split(w):
    """Return (a, b) if w is two common words glued together, else None."""
    for i in range(3, len(w) - 2):
        a, b = w[:i], w[i:]
        if a in AFFIX_LIKE or max(len(a), len(b)) < 4:
            continue
        if a in CORE and b in CORE:
            return a, b
    return None


def lint(raw):
    name = raw.strip()
    fails, warns = [], []
    low = name.lower()

    if not name:
        return name, "FAIL", ["empty"]
    if re.search(r"[\s\-_.\d]", name):
        fails.append("not a single token (space, hyphen, dot, underscore or digit)")
    if not re.fullmatch(r"[A-Za-z]+", re.sub(r"[\s\-_.\d]", "", name) or "x"):
        fails.append("contains non-letter characters")
    if re.search(r"[a-z][A-Z]", name):
        fails.append("CamelCase internal capital (reads as two words)")

    letters = re.sub(r"[^a-z]", "", low)
    is_dict_word = letters in WORDS

    if letters in SLOP:
        fails.append("overused AI/tech cliche (slop list)")

    if len(letters) < 3:
        fails.append("shorter than 3 letters")
    elif len(letters) > 12:
        fails.append("longer than 12 letters")
    elif len(letters) > 9:
        warns.append("long (over 9 letters); hard to fit in a logo and a URL")

    if len(letters) >= 6:
        split = compound_split(letters)
        if split and not is_dict_word:
            fails.append(f"glued compound: '{split[0]}' + '{split[1]}'")
        elif split:
            # Real compound words (carpet, sunflower) and famous brands (dropbox)
            # are in the word list. Flag them so the compound shape gets a second look.
            warns.append(f"reads as two words: '{split[0]}' + '{split[1]}'")

    if not is_dict_word:
        for suf in BANNED_SUFFIXES:
            stem = letters[: -len(suf)]
            if letters.endswith(suf) and len(stem) >= 3 and letters != suf:
                # Short stems must be very common words (so coined names like
                # Attio survive); longer stems can be any dictionary word (Ledgerly).
                real_stem = stem in CORE or (len(stem) >= 4 and stem in WORDS)
                if real_stem or stem in SLOP or stem in BANNED_PREFIXES:
                    fails.append(f"word + stuck-on suffix '-{suf}'")
                    break
        for pre in BANNED_PREFIXES:
            rest = letters[len(pre):]
            if letters.startswith(pre) and len(rest) >= 3:
                warns.append(f"cliche prefix '{pre}-'")
                break
        for slop in SLOP:
            if len(slop) >= 4 and slop in letters and letters != slop:
                warns.append(f"contains slop fragment '{slop}'")
                break

    if not re.search(r"[aeiouy]", letters):
        fails.append("no vowels; can't be pronounced from sight")
    # Collapse digraphs (ch, th, tch...) to one sound, and ignore clusters that end in
    # l or r (-ple, -tle, str-), which English speakers say without effort.
    sounds = letters
    for dg in ("tch", "ch", "sh", "th", "ph", "wh", "ck", "ng", "gh"):
        sounds = sounds.replace(dg, "X")
    clusters = [c for c in re.findall(r"[^aeiouy]{3,}", sounds) if not c.endswith(("l", "r"))]
    if any(len(c) >= 4 for c in clusters):
        warns.append("4+ consonant sounds in a row; may be hard to say")
    elif clusters:
        warns.append(f"awkward consonant cluster '{clusters[0]}'")
    if re.search(r"[^aeiouy]r$", letters) and (letters[:-1] + "er") in WORDS:
        warns.append("vowel-dropped spelling (Flickr/Tumblr style)")
    if re.search(r"(.)\1\1", letters):
        warns.append("triple letter")

    status = "FAIL" if fails else ("WARN" if warns else "PASS")
    return name, status, fails + warns


def main(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if argv[:1] == ["--file"] and len(argv) > 1:
        names = [l.strip() for l in Path(argv[1]).read_text().splitlines() if l.strip()]
    else:
        names = argv
    if not names:
        print(__doc__)
        return 1
    if not WORDS:
        print("warning: assets/words.txt missing; compound detection disabled", file=sys.stderr)

    results = [lint(n) for n in names]
    if as_json:
        print(json.dumps([{"name": n, "status": s, "reasons": r} for n, s, r in results], indent=2))
    else:
        width = max(len(n) for n, _, _ in results)
        for n, s, r in results:
            print(f"{s:4}  {n:<{width}}  {'; '.join(r)}")
        counts = {k: sum(1 for _, s, _ in results if s == k) for k in ("PASS", "WARN", "FAIL")}
        print(f"\n{counts['PASS']} pass, {counts['WARN']} warn, {counts['FAIL']} fail")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

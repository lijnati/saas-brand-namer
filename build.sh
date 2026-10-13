#!/usr/bin/env bash
# Package the skill (SKILL.md, scripts, assets only) into dist/saas-brand-namer.skill
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist
python3 - <<'PY'
import zipfile, pathlib
root = pathlib.Path("skills/saas-brand-namer")
name = "saas-brand-namer"
with zipfile.ZipFile(f"dist/{name}.skill", "w", zipfile.ZIP_DEFLATED) as z:
    for p in [root / "SKILL.md", *sorted((root / "scripts").rglob("*.py")), *sorted((root / "assets").rglob("*.txt"))]:
        z.write(p, f"{name}/{p.relative_to(root).as_posix()}")
print(f"built dist/{name}.skill")
PY

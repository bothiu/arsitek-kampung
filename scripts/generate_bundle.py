#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE_DIR = ROOT.parent / "arsitek-kampung-install-bundle"

SOURCE_REPO_URL = "https://github.com/bothiu/arsitek-kampung"
BUNDLE_REPO_URL = "https://github.com/bothiu/arsitek-kampung-install-bundle"
RAW_BUNDLE_SKILL_URL = (
    "https://raw.githubusercontent.com/bothiu/arsitek-kampung-install-bundle/main/SKILL.md"
)

BUNDLE_NOTE = (
    "> **Bundle note:** ini adalah distribusi single-file untuk installer yang saat ini hanya menyalin `SKILL.md`.\n"
    "> Konten pendukung dari `references/report-template.md` dan `examples/endpoint-inventory.md` sudah di-embed ke file ini supaya tetap ikut terbawa saat install."
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def inject_bundle_note(skill_text: str) -> str:
    marker = "# Arsitek Kampung\n\n## Overview"
    replacement = f"# Arsitek Kampung\n\n{BUNDLE_NOTE}\n\n## Overview"
    if marker not in skill_text:
        raise SystemExit("Could not locate title/overview marker in source SKILL.md")
    return skill_text.replace(marker, replacement, 1)


def embed_support_files(skill_text: str, report_template: str, example_output: str) -> str:
    pattern = re.compile(r"## Support Files\n.*?\n## Verification Checklist", re.S)
    replacement = (
        "## Support Files\n\n"
        "Distribusi bundle ini **meng-embed** file pendukung langsung ke dalam `SKILL.md` karena beberapa installer komunitas hanya menyalin satu file.\n\n"
        "Sumber canonical tetap ada di repo utama:\n"
        f"- `{SOURCE_REPO_URL}`\n\n"
        "### Embedded: `references/report-template.md`\n\n"
        f"```md\n{report_template.rstrip()}\n```\n\n"
        "### Embedded: `examples/endpoint-inventory.md`\n\n"
        f"```md\n{example_output.rstrip()}\n```\n\n"
        "## Verification Checklist"
    )
    new_skill, count = pattern.subn(replacement, skill_text)
    if count != 1:
        raise SystemExit("Failed to rewrite Support Files section")
    return new_skill


def generate_bundle_skill(skill_text: str, report_template: str, example_output: str) -> str:
    skill_text = inject_bundle_note(skill_text)
    skill_text = embed_support_files(skill_text, report_template, example_output)
    return skill_text


def generate_bundle_readme() -> str:
    return f"""# Arsitek Kampung — Install Bundle

Companion repo untuk distribusi **single-file** skill `arsitek-kampung`.

> File di repo ini di-generate otomatis dari repo sumber utama.

Tujuan repo ini: mengatasi installer yang saat ini hanya menyalin `SKILL.md`, sehingga file pendukung seperti `references/` dan `examples/` tidak ikut kebawa. Di bundle ini, konten pendukung sudah **di-embed langsung** ke dalam `SKILL.md`.

## Canonical source

Repo sumber utama:
- {SOURCE_REPO_URL}

## Install ke Hermes

### Raw URL
```bash
hermes skills install {RAW_BUNDLE_SKILL_URL}
```

### npx skills
```bash
npx -y skills add bothiu/arsitek-kampung-install-bundle --skill arsitek-kampung --agent hermes-agent --global --yes
```

## Regenerate bundle

Dari repo source:
```bash
python3 scripts/generate_bundle.py
```

Default output target:
- `{DEFAULT_BUNDLE_DIR}`

## Catatan

- Nama skill tetap `arsitek-kampung`.
- Repo ini adalah **bundle distribution**, bukan source of truth.
- Kalau skill dengan nama yang sama sudah terpasang, installer mungkin butuh `--force` untuk replace install lama.
"""


def main() -> None:
    bundle_dir = DEFAULT_BUNDLE_DIR

    source_skill = read(ROOT / "SKILL.md")
    report_template = read(ROOT / "references" / "report-template.md")
    example_output = read(ROOT / "examples" / "endpoint-inventory.md")
    license_text = read(ROOT / "LICENSE")

    generated_skill = generate_bundle_skill(source_skill, report_template, example_output)
    generated_readme = generate_bundle_readme()

    bundle_dir.mkdir(parents=True, exist_ok=True)
    write(bundle_dir / "SKILL.md", generated_skill)
    write(bundle_dir / "README.md", generated_readme)
    write(bundle_dir / "LICENSE", license_text)

    print(f"Generated bundle into: {bundle_dir}")
    print("Files:")
    for name in ["SKILL.md", "README.md", "LICENSE"]:
        print(f"- {bundle_dir / name}")


if __name__ == "__main__":
    main()

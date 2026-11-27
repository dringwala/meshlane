"""Documentation checks for this repository. Standard library only.

1. Every relative link in a Markdown file points to a file that exists.
2. The YAML examples in docs/architecture.md are identical to the example
   files that CI validates.

Run from anywhere:  python .github/scripts/check_docs.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "docs/spikes/oq-03-odps-odcs-validation"
ARCHITECTURE_EXAMPLES = ["data-product.yaml", "contracts/shipments.odcs.yaml"]
SKIP = {".git", ".venv", "venv", "node_modules"}
LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.S | re.M)


def markdown_files():
    for path in sorted(ROOT.rglob("*.md")):
        if not SKIP & set(path.relative_to(ROOT).parts):
            yield path


def broken_links():
    count, errors = 0, []
    for md in markdown_files():
        text = FENCE.sub("", md.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            count += 1
            if not (md.parent / target.split("#")[0]).exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link {target}")
    return count, errors


def example_drift():
    text = (ROOT / "docs/architecture.md").read_text(encoding="utf-8")
    blocks = re.findall(r"^```yaml\n(.*?)^```", text, re.S | re.M)
    if len(blocks) != len(ARCHITECTURE_EXAMPLES):
        return [
            f"docs/architecture.md: expected {len(ARCHITECTURE_EXAMPLES)} yaml blocks, found {len(blocks)}"
        ]
    return [
        f"docs/architecture.md: yaml block {i} differs from {(EXAMPLES / name).relative_to(ROOT)}"
        for i, (block, name) in enumerate(zip(blocks, ARCHITECTURE_EXAMPLES), 1)
        if block != (EXAMPLES / name).read_text(encoding="utf-8")
    ]


def main():
    count, errors = broken_links()
    errors += example_drift()
    for error in errors:
        print(f"ERROR  {error}")
    print(f"{count} relative links checked, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

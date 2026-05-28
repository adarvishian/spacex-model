"""CLI: audit / Model Translation Log — PRD §11.1."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from spacex_model.audit.translation_log import generate_translation_log


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Model Translation Log and architecture diagram (PRD §11.1)"
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=None,
        help="Output directory (default: repo docs/)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if generated CSV differs from checked-in copy",
    )
    args = parser.parse_args(argv)

    docs_dir = args.docs_dir or (_repo_root() / "docs")
    csv_path, md_path = generate_translation_log(docs_dir)

    if args.check:
        import subprocess

        result = subprocess.run(
            ["git", "diff", "--quiet", str(csv_path), str(md_path)],
            cwd=_repo_root(),
            capture_output=True,
        )
        if result.returncode != 0:
            print(
                f"Audit artifacts drift detected: {csv_path.name}, {md_path.name}. "
                "Run: spacex-audit",
                file=sys.stderr,
            )
            return 1

    print(f"Wrote {csv_path} ({csv_path.stat().st_size} bytes)")
    print(f"Wrote {md_path} ({md_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

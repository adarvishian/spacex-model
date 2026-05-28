"""Uvicorn entry point for the Mach33 SpaceX Model API."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Mach33 SpaceX Model API server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="Dev auto-reload")
    args = parser.parse_args(argv)

    import uvicorn

    uvicorn.run(
        "spacex_model.service.api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

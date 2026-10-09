"""Guards for the data-source rules.

Markdown may name Transfermarkt only to forbid scraping and training on it.
No host, client module, or valuation-scraping dependency may appear anywhere.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    "node_modules",
    ".next",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
}
BANNED_HOSTS = tuple(
    "transfermarkt." + suffix for suffix in ("com", "de", "co.uk", "world")
)
BANNED_DEPENDENCIES = ("soccerdata", "worldfootballr")
MANIFEST_NAMES = {
    "pyproject.toml",
    "requirements-ci.txt",
    "requirements.txt",
    "package.json",
    "pnpm-lock.yaml",
}


def _files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.parts):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        yield path


def test_no_transfermarkt_host_or_module() -> None:
    for path in _files():
        lowered_name = path.name.lower()
        assert "transfermarkt" not in lowered_name
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for host in BANNED_HOSTS:
            assert host not in text, f"{host} found in {path}"
        if "transfermarkt" in text:
            assert path.suffix.lower() == ".md", path
            assert any(token in text for token in ("never", "forbidden", "do not")), path


def test_manifests_do_not_depend_on_valuation_scrapers() -> None:
    for path in _files():
        if path.name not in MANIFEST_NAMES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for name in BANNED_DEPENDENCIES:
            assert name not in text, f"{name} found in {path}"
        assert "transfermarkt" not in text


def test_ingest_does_not_import_an_http_client() -> None:
    source_root = ROOT / "packages" / "ingest" / "src"
    text = "\n".join(
        path.read_text(encoding="utf-8") for path in source_root.rglob("*.py")
    )
    for banned in ("import httpx", "import requests", "urllib.request", "urlopen"):
        assert banned not in text

"""Environment configuration for ingest workers."""

import os
from collections.abc import Mapping
from dataclasses import dataclass


def _flag(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class IngestConfig:
    """Settings for football-API and ClubElo stubs.

    Missing variables fall back to the free-first defaults: a stub football
    provider and ClubElo fetch disabled. A key is never required to construct
    this object.
    """

    football_api_provider: str
    football_api_key: str | None
    clubelo_base_url: str
    clubelo_fetch_enabled: bool
    database_url: str | None

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "IngestConfig":
        source = os.environ if env is None else env
        provider = (source.get("FOOTBALL_API_PROVIDER") or "stub").strip() or "stub"
        key = (source.get("FOOTBALL_API_KEY") or "").strip() or None
        base_url = (source.get("CLUBELO_BASE_URL") or "http://api.clubelo.com").rstrip("/")
        return cls(
            football_api_provider=provider,
            football_api_key=key,
            clubelo_base_url=base_url,
            clubelo_fetch_enabled=_flag(source.get("CLUBELO_FETCH_ENABLED")),
            database_url=(source.get("DATABASE_URL") or "").strip() or None,
        )

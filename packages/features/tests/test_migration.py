from pathlib import Path

MIGRATION = (
    Path(__file__).resolve().parents[1] / "migrations" / "001_init.sql"
)


def test_migration_declares_core_tables() -> None:
    sql = MIGRATION.read_text(encoding="utf-8")
    for table in (
        "players",
        "player_external_ids",
        "features_snapshot",
        "predictions",
    ):
        assert f"CREATE TABLE {table}" in sql
    assert "horizon_months = 6" in sql
    assert "football_api" in sql
    assert "clubelo" in sql

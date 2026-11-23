"""Cấu hình đường dẫn. Ghi đè bằng biến môi trường QUYCHE_* hoặc file .env."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="QUYCHE_", env_file=".env", extra="ignore")

    raw_dir: Path = Path("data/raw")
    chunks_path: Path = Path("data/processed/chunks.jsonl")
    questions_path: Path = Path("eval/questions.jsonl")
    reports_dir: Path = Path("eval/reports")


def get_settings() -> Settings:
    return Settings()

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    mock_api_url: str = os.getenv("API_URL", "")
    mock_api_key: str = os.getenv("API_KEY", "")


    raw_dir: Path = ROOT/"data"/"incremental"/"day_2026-07-01"
    staging_dir: Path = ROOT/"data"/"staging"
    reject_dir: Path = ROOT/"data"/"reject"
    metadata_dir: Path = ROOT/"data"/"metadata"
    report_dir: Path = ROOT/"data"/"report"

SETTINGS = Settings()
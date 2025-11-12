import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Settings:
    DEFAULT_LOCALE = "pt_BR"
    DEFAULT_SEED = 42
    DEFAULT_BATCH_SIZE = 50
    MAX_BATCH_SIZE = 10000
    OUTPUT_DIR = Path("output")
    MIN_AGE = 18
    MAX_AGE = 80
    MAX_VALID_AGE = 150


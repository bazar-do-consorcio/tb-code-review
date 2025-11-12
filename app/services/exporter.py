import csv
import json
import logging
from pathlib import Path
from typing import List

from ..models.person import Person
from ..models.enums import DataFormat

logger = logging.getLogger(__name__)


class DataExporter:
    @staticmethod
    def export_to_json(persons: List[Person], filepath: str) -> bool:
        try:
            data = [p.to_dict() for p in persons]
            file_path = Path(filepath)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Dados exportados para {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao exportar JSON: {e}")
            return False

    @staticmethod
    def export_to_csv(persons: List[Person], filepath: str) -> bool:
        try:
            file_path = Path(filepath)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if not persons:
                logger.warning("Lista vazia, nada para exportar")
                return False

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "name",
                        "email",
                        "age",
                        "country",
                        "phone",
                        "street",
                        "city",
                        "state",
                        "zip_code",
                    ],
                )
                writer.writeheader()
                for p in persons:
                    row = p.to_dict()
                    row.update(row["address"])
                    del row["address"]
                    writer.writerow(row)

            logger.info(f"Dados exportados para {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            return False

    @staticmethod
    def export(persons: List[Person], filepath: str, data_format: DataFormat) -> bool:
        if data_format == DataFormat.JSON:
            return DataExporter.export_to_json(persons, filepath)
        elif data_format == DataFormat.CSV:
            return DataExporter.export_to_csv(persons, filepath)
        else:
            logger.error(f"Formato não suportado: {data_format}")
            return False


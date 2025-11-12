import logging
from pathlib import Path

from .config.settings import Settings
from .models.enums import DataFormat
from .services.generator import FakeDataGenerator
from .services.exporter import DataExporter

logger = logging.getLogger(__name__)


def main():
    try:
        generator = FakeDataGenerator(
            locale=Settings.DEFAULT_LOCALE, seed=Settings.DEFAULT_SEED
        )
        exporter = DataExporter()

        logger.info("=== Gerador de Dados Fake ===")

        logger.info("Gerando dados fake individuais")
        person = generator.generate_person()
        logger.info(f"Pessoa gerada: {person}")

        logger.info("Gerando lote de dados fake")
        batch_data = generator.generate_batch(Settings.DEFAULT_BATCH_SIZE)
        logger.info(f"Total de registros gerados: {len(batch_data)}")

        logger.info("Exibindo primeiros 5 registros:")
        for idx, record in enumerate(batch_data[:5], 1):
            logger.info(f"Registro {idx}: {record}")

        logger.info("Filtrando por país (Brasil):")
        brazilian_persons = generator.filter_by_country(batch_data, "Brazil")
        logger.info(f"Encontrados {len(brazilian_persons)} brasileiros")

        logger.info("Filtrando por faixa etária (25-35 anos):")
        young_adults = generator.filter_by_age_range(batch_data, 25, 35)
        logger.info(f"Encontradas {len(young_adults)} pessoas entre 25-35 anos")

        logger.info("Estatísticas gerais:")
        stats = generator.get_statistics(batch_data)
        logger.info(f"Total: {stats.get('total')}")
        logger.info(f"Idade média: {stats.get('average_age', 0):.2f} anos")
        logger.info(f"Idade mínima: {stats.get('min_age')} anos")
        logger.info(f"Idade máxima: {stats.get('max_age')} anos")

        Settings.OUTPUT_DIR.mkdir(exist_ok=True)

        logger.info("Exportando dados...")
        exporter.export(
            batch_data,
            str(Settings.OUTPUT_DIR / "fake_data.json"),
            DataFormat.JSON,
        )
        exporter.export(
            batch_data,
            str(Settings.OUTPUT_DIR / "fake_data.csv"),
            DataFormat.CSV,
        )

        logger.info(
            f"Total de pessoas geradas nesta sessão: {generator.generated_count}"
        )

    except Exception as e:
        logger.error(f"Erro ao gerar dados fake: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

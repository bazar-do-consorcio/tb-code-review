import logging
from typing import Dict, List, Optional
from faker import Faker
from .request_service import error_request_import

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FakeDataGenerator:
    def __init__(self, locale: str = "pt_BR", seed: Optional[int] = None):
        self.faker = Faker(locale)
        if seed is not None:
            Faker.seed(seed)
        self.locale = locale

    def generate_name(self) -> str:
        return self.faker.name()

    def generate_email(self) -> str:
        return self.faker.email()

    def generate_country(self) -> str:
        return self.faker.country()

    def generate_age(self, min_age: int = 18, max_age: int = 80) -> int:
        return self.faker.random_int(min=min_age, max=max_age)

    def generate_phone(self) -> str:
        return self.faker.phone_number()

    def generate_address(self) -> Dict[str, str]:
        return {
            "street": self.faker.street_address(),
            "city": self.faker.city(),
            "state": self.faker.state(),
            "zip_code": self.faker.postcode(),
            "country": self.faker.country(),
        }

    def generate_fake_data(self) -> Dict:
        return {
            "name": self.generate_name(),
            "email": self.generate_email(),
            "age": self.generate_age(),
            "country": self.generate_country(),
            "phone": self.generate_phone(),
            "address": self.generate_address(),
        }

    def generate_batch(self, count: int) -> List[Dict]:
        if count <= 0:
            logger.warning("Count deve ser maior que zero. Retornando lista vazia.")
            return []

        logger.info(f"Gerando {count} registros de dados fake")
        return [self.generate_fake_data() for _ in range(count)]


def main():
    try:
        generator = FakeDataGenerator(locale="pt_BR")

        logger.info("Gerando dados fake individuais")
        fake_data = generator.generate_fake_data()
        logger.info(f"Dados gerados: {fake_data}")

        logger.info("Gerando lote de dados fake")
        batch_data = generator.generate_batch(5)
        logger.info(f"Total de registros gerados: {len(batch_data)}")

        for idx, record in enumerate(batch_data, 1):
            logger.info(f"Registro {idx}: {record['name']} - {record['email']}")

        logger.info("Rodando função com erro de import")
        error_request_import()

    except Exception as e:
        logger.error(f"Erro ao gerar dados fake: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

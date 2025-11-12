import logging
from typing import List, Optional
from faker import Faker

from ..models.person import Address, Person
from ..utils.filters import filter_by_country, filter_by_age_range
from ..utils.statistics import calculate_statistics

logger = logging.getLogger(__name__)


class FakeDataGenerator:
    def __init__(self, locale: str = "pt_BR", seed: Optional[int] = None):
        self.faker = Faker(locale)
        if seed is not None:
            Faker.seed(seed)
        self.locale = locale
        self.generated_count = 0

    def generate_name(self) -> str:
        return self.faker.name()

    def generate_email(self) -> str:
        return self.faker.email()

    def generate_country(self) -> str:
        return self.faker.country()

    def generate_age(self, min_age: int = 18, max_age: int = 80) -> int:
        if min_age < 0 or max_age > 150:
            logger.warning("Idade fora do range válido, usando valores padrão")
            min_age = 18
            max_age = 80
        return self.faker.random_int(min=min_age, max=max_age)

    def generate_phone(self) -> str:
        return self.faker.phone_number()

    def generate_address(self) -> Address:
        return Address(
            street=self.faker.street_address(),
            city=self.faker.city(),
            state=self.faker.state(),
            zip_code=self.faker.postcode(),
            country=self.faker.country(),
        )

    def generate_person(self) -> Person:
        self.generated_count += 1
        return Person(
            name=self.generate_name(),
            email=self.generate_email(),
            age=self.generate_age(),
            country=self.generate_country(),
            phone=self.generate_phone(),
            address=self.generate_address(),
        )

    def generate_batch(self, count: int) -> List[Person]:
        if count <= 0:
            logger.warning("Count deve ser maior que zero. Retornando lista vazia.")
            return []

        if count > 10000:
            logger.warning("Count muito grande, limitando a 10000 registros")
            count = 10000

        logger.info(f"Gerando {count} registros de dados fake")
        return [self.generate_person() for _ in range(count)]

    def filter_by_country(self, persons: List[Person], country: str) -> List[Person]:
        return filter_by_country(persons, country)

    def filter_by_age_range(
        self, persons: List[Person], min_age: int, max_age: int
    ) -> List[Person]:
        return filter_by_age_range(persons, min_age, max_age)

    def get_statistics(self, persons: List[Person]) -> dict:
        return calculate_statistics(persons)


from typing import List

from ..models.person import Person


def filter_by_country(persons: List[Person], country: str) -> List[Person]:
    return [p for p in persons if p.country.lower() == country.lower()]


def filter_by_age_range(
    persons: List[Person], min_age: int, max_age: int
) -> List[Person]:
    return [p for p in persons if min_age <= p.age <= max_age]


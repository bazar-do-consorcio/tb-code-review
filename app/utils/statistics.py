from typing import Dict, List

from ..models.person import Person


def calculate_statistics(persons: List[Person]) -> Dict:
    if not persons:
        return {}

    ages = [p.age for p in persons]
    countries = {}
    for p in persons:
        countries[p.country] = countries.get(p.country, 0) + 1

    return {
        "total": len(persons),
        "average_age": sum(ages) / len(ages),
        "min_age": min(ages),
        "max_age": max(ages),
        "countries_distribution": countries,
    }


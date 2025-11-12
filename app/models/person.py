from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

    def __str__(self) -> str:
        return f"{self.street}, {self.city} - {self.state}, {self.zip_code}, {self.country}"


@dataclass
class Person:
    name: str
    email: str
    age: int
    country: str
    phone: str
    address: Address

    def __str__(self) -> str:
        return f"{self.name} ({self.email}) - {self.age} anos"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "country": self.country,
            "phone": self.phone,
            "address": asdict(self.address),
        }


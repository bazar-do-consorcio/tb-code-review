import csv
import json
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from faker import Faker

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

    def generate_company(self) -> Dict:
        """Gera dados de uma empresa fake"""
        return {
            "company_name": self.faker.company(),
            "catch_phrase": self.faker.catch_phrase(),
            "bs": self.faker.bs(),
            "email": self.faker.company_email(),
            "website": self.faker.url(),
            "phone": self.faker.phone_number(),
            "address": self.generate_address(),
        }


class DataExporter:
    """Classe para exportar dados em diferentes formatos"""

    @staticmethod
    def export_to_json(data: List[Dict], filename: str = None) -> str:
        """Exporta dados para arquivo JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fake_data_{timestamp}.json"

        filepath = Path(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Dados exportados para JSON: {filepath.absolute()}")
        return str(filepath.absolute())

    @staticmethod
    def export_to_csv(data: List[Dict], filename: str = None) -> str:
        """Exporta dados para arquivo CSV"""
        if not data:
            logger.warning("Nenhum dado para exportar")
            return ""

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fake_data_{timestamp}.csv"

        filepath = Path(filename)

        # Flatten nested dictionaries (like address)
        flattened_data = []
        for record in data:
            flat_record = {}
            for key, value in record.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        flat_record[f"{key}_{sub_key}"] = sub_value
                else:
                    flat_record[key] = value
            flattened_data.append(flat_record)

        fieldnames = flattened_data[0].keys() if flattened_data else []

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_data)

        logger.info(f"Dados exportados para CSV: {filepath.absolute()}")
        return str(filepath.absolute())


class DataStatistics:
    """Classe para calcular estatísticas dos dados gerados"""

    @staticmethod
    def calculate_stats(data: List[Dict]) -> Dict:
        """Calcula estatísticas dos dados gerados"""
        if not data:
            return {}

        ages = [record.get("age", 0) for record in data if "age" in record]
        countries = [record.get("country", "") for record in data if "country" in record]

        stats = {
            "total_records": len(data),
            "age_stats": {},
            "country_distribution": {},
        }

        if ages:
            stats["age_stats"] = {
                "min": min(ages),
                "max": max(ages),
                "average": round(sum(ages) / len(ages), 2),
                "median": sorted(ages)[len(ages) // 2],
            }

        if countries:
            country_counter = Counter(countries)
            stats["country_distribution"] = dict(country_counter.most_common(10))

        return stats

    @staticmethod
    def print_stats(stats: Dict):
        """Imprime estatísticas de forma formatada"""
        print("\n" + "=" * 50)
        print("📊 ESTATÍSTICAS DOS DADOS GERADOS")
        print("=" * 50)

        print(f"\n📝 Total de registros: {stats.get('total_records', 0)}")

        age_stats = stats.get("age_stats", {})
        if age_stats:
            print("\n👥 Estatísticas de Idade:")
            print(f"   • Idade mínima: {age_stats.get('min', 'N/A')} anos")
            print(f"   • Idade máxima: {age_stats.get('max', 'N/A')} anos")
            print(f"   • Idade média: {age_stats.get('average', 'N/A')} anos")
            print(f"   • Idade mediana: {age_stats.get('median', 'N/A')} anos")

        country_dist = stats.get("country_distribution", {})
        if country_dist:
            print("\n🌍 Distribuição por País (Top 10):")
            for country, count in country_dist.items():
                percentage = (count / stats.get("total_records", 1)) * 100
                print(f"   • {country}: {count} ({percentage:.1f}%)")

        print("=" * 50 + "\n")


class DataValidator:
    """Classe para validar dados gerados"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato básico de email"""
        return "@" in email and "." in email.split("@")[1]

    @staticmethod
    def validate_age(age: int, min_age: int = 0, max_age: int = 150) -> bool:
        """Valida idade dentro de limites razoáveis"""
        return min_age <= age <= max_age

    @staticmethod
    def validate_record(record: Dict) -> Dict[str, bool]:
        """Valida um registro completo"""
        validation = {
            "email_valid": DataValidator.validate_email(record.get("email", "")),
            "age_valid": DataValidator.validate_age(record.get("age", 0)),
            "has_name": bool(record.get("name")),
            "has_address": bool(record.get("address")),
        }
        validation["all_valid"] = all(validation.values())
        return validation

    @staticmethod
    def validate_batch(data: List[Dict]) -> Dict:
        """Valida um lote de dados"""
        results = {
            "total": len(data),
            "valid": 0,
            "invalid": 0,
            "invalid_records": [],
        }

        for idx, record in enumerate(data):
            validation = DataValidator.validate_record(record)
            if validation["all_valid"]:
                results["valid"] += 1
            else:
                results["invalid"] += 1
                results["invalid_records"].append(
                    {"index": idx, "record": record, "validation": validation}
                )

        return results

    @staticmethod
    def print_validation_results(results: Dict):
        """Imprime resultados da validação"""
        print("\n" + "=" * 50)
        print("✅ RESULTADOS DA VALIDAÇÃO")
        print("=" * 50)
        print(f"\n📊 Total de registros: {results['total']}")
        print(f"✅ Registros válidos: {results['valid']}")
        print(f"❌ Registros inválidos: {results['invalid']}")

        if results["invalid_records"]:
            print("\n⚠️  Registros com problemas:")
            for item in results["invalid_records"][:5]:  # Mostra apenas os 5 primeiros
                print(f"\n   Registro #{item['index']}:")
                for check, status in item["validation"].items():
                    status_icon = "✅" if status else "❌"
                    print(f"   {status_icon} {check}: {status}")

        print("=" * 50 + "\n")


def interactive_menu():
    """Menu interativo para o usuário"""
    print("\n" + "=" * 60)
    print("🎲 GERADOR DE DADOS FAKE - MENU INTERATIVO")
    print("=" * 60)
    print("\n1. Gerar dados individuais")
    print("2. Gerar lote de dados")
    print("3. Gerar dados de empresa")
    print("4. Exportar dados para JSON")
    print("5. Exportar dados para CSV")
    print("6. Ver estatísticas dos dados")
    print("7. Validar dados gerados")
    print("8. Demo completo (gera, valida, exporta e mostra stats)")
    print("0. Sair")
    print("\n" + "=" * 60)


def main():
    try:
        generator = FakeDataGenerator(locale="pt_BR")
        exporter = DataExporter()
        stats_calculator = DataStatistics()
        validator = DataValidator()

        # Dados em memória para operações
        current_data = []

        while True:
            interactive_menu()
            choice = input("\nEscolha uma opção: ").strip()

            if choice == "0":
                print("\n👋 Até logo!")
                break

            elif choice == "1":
                logger.info("Gerando dados fake individuais")
                fake_data = generator.generate_fake_data()
                current_data = [fake_data]
                print("\n✅ Dados gerados:")
                print(json.dumps(fake_data, ensure_ascii=False, indent=2))

            elif choice == "2":
                count = input("Quantos registros deseja gerar? (padrão: 10): ").strip()
                count = int(count) if count.isdigit() else 10
                logger.info(f"Gerando lote de {count} registros")
                current_data = generator.generate_batch(count)
                print(f"\n✅ {len(current_data)} registros gerados com sucesso!")

            elif choice == "3":
                logger.info("Gerando dados de empresa")
                company_data = generator.generate_company()
                current_data = [company_data]
                print("\n✅ Dados da empresa gerados:")
                print(json.dumps(company_data, ensure_ascii=False, indent=2))

            elif choice == "4":
                if not current_data:
                    print("\n⚠️  Nenhum dado gerado ainda. Gere dados primeiro!")
                else:
                    filename = input("Nome do arquivo (Enter para usar padrão): ").strip()
                    filename = filename if filename else None
                    filepath = exporter.export_to_json(current_data, filename)
                    print(f"\n✅ Dados exportados: {filepath}")

            elif choice == "5":
                if not current_data:
                    print("\n⚠️  Nenhum dado gerado ainda. Gere dados primeiro!")
                else:
                    filename = input("Nome do arquivo (Enter para usar padrão): ").strip()
                    filename = filename if filename else None
                    filepath = exporter.export_to_csv(current_data, filename)
                    print(f"\n✅ Dados exportados: {filepath}")

            elif choice == "6":
                if not current_data:
                    print("\n⚠️  Nenhum dado gerado ainda. Gere dados primeiro!")
                else:
                    stats = stats_calculator.calculate_stats(current_data)
                    stats_calculator.print_stats(stats)

            elif choice == "7":
                if not current_data:
                    print("\n⚠️  Nenhum dado gerado ainda. Gere dados primeiro!")
                else:
                    validation_results = validator.validate_batch(current_data)
                    validator.print_validation_results(validation_results)

            elif choice == "8":
                print("\n🚀 Executando demo completo...")
                count = input("Quantos registros deseja gerar? (padrão: 20): ").strip()
                count = int(count) if count.isdigit() else 20

                # Gerar dados
                logger.info(f"Gerando {count} registros para demo")
                current_data = generator.generate_batch(count)
                print(f"\n✅ {len(current_data)} registros gerados")

                # Validar
                validation_results = validator.validate_batch(current_data)
                validator.print_validation_results(validation_results)

                # Estatísticas
                stats = stats_calculator.calculate_stats(current_data)
                stats_calculator.print_stats(stats)

                # Exportar
                json_file = exporter.export_to_json(current_data)
                csv_file = exporter.export_to_csv(current_data)
                print(f"\n💾 Arquivos exportados:")
                print(f"   • JSON: {json_file}")
                print(f"   • CSV: {csv_file}")

            else:
                print("\n❌ Opção inválida! Tente novamente.")

            if choice != "0":
                input("\nPressione Enter para continuar...")

    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
    except Exception as e:
        logger.error(f"Erro ao executar programa: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

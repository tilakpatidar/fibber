from typing import Dict, Callable, Any
from faker import Faker

fake = Faker()


def _seed_and_gen(value, fake_generate: Callable[[], Any]) -> Any:
    fake.seed_instance(value)
    return fake_generate()


def generate(fake_generate: Callable[[], Any]) -> Callable[[str], Any]:
    return lambda value: _seed_and_gen(value, fake_generate)


mapping: Dict[str, Callable[[str], Any]] = {
    "customer_id": generate(lambda: fake.numerify("#" * 10)),
    "company_name": generate(lambda: fake.company()),
    "contact_name": generate(lambda: fake.name()),
    "contact_title": generate(lambda: fake.job()),
    "address": generate(lambda: fake.address()),
    "city": generate(lambda: fake.city()),
    "region": generate(lambda: fake.city()),
    "postal_code": generate(lambda: fake.zipcode()),
    "country": generate(lambda: fake.country()),
    "phone": generate(lambda: fake.numerify("#" * 10)),
    "fax": generate(lambda: fake.numerify("#" * 10)),
}

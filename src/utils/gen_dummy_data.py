from faker import Faker
from faker.providers import DynamicProvider
from faker.exceptions import UniquenessException

from datetime import timedelta, date
import random

from utils.types import TypeCourse, TypeUser

from structs.pqueue import PQueue
from structs.product import Product
from structs.payment import (
    COURSES_AVAILABLE,
    USERS_CATEGORIES,
    Payment,
)

fruits: DynamicProvider = DynamicProvider(
    provider_name="fruits",
    elements=[
        # Frutas Inteiras
        "Banana Nanica",
        "Maçã Gala",
        "Pera",
        "Goiaba",
        "Tangerina",
        # Copos de Fruta
        "Salada de Frutas (Copo 200ml)",
        "Melancia em Cubos",
        "Mamão Papaia fatiado",
        "Abacaxi com Raspas de Limão",
        "Uva Sem Semente (Potinho)",
        # Saudáveis
        "Açaí no Copo",
        "Morango com Leite Condensado",
        "Coco Gelado (Pedaços)",
        # --- Frutas Tropicais e de Época ---
        "Manga Palmer Fatiada",
        "Caqui (Unidade)",
        "Ameixa Vermelha",
        "Jabuticaba (Saquinho)",
        "Pitaya Rosa em Cubos",
        "Caju Inteiro",
        # --- Combinações com Iogurte/Cereais ---
        "Iogurte com Pedaços de Morango",
        "Banana com Granola e Mel",
        "Maçã com Canela (Pote)",
        "Abacate com Açúcar e Limão",
        # --- Frutas Secas ---
        "Mix de Frutas Secas (Damasco e Uva Passa)",
        "Chips de Banana",
        "Tâmara Recheada com Castanha",
        "Maçã Desidratada",
        # --- Suco/Vitamina ---
        "Polpa de Acerola Fresca",
        "Maracujá no Corte",
        "Limão para Suco",
    ],
)

fake: Faker = Faker("pt_BR")

fake.add_provider(fruits)

# expiry_counter = 0


def gen_product() -> Product:
    # global expiry_counter
    # expiry_counter += 10

    d_buy: date = fake.date_between(start_date="-30d", end_date="+30d")
    d_exp: date = d_buy + timedelta(days=fake.random_int(min=1, max=100))

    # d_buy = date.today()
    # d_exp = d_buy + timedelta(days=expiry_counter)
    n_name: str = "Kiwi"
    try:
        n_name = fake.unique.fruits()
    except UniquenessException:
        fake.unique.clear()
        n_name = fake.unique.fruits()

    return Product(
        name=n_name,
        price_buy=fake.random_int(min=5, max=50) * 100,
        price_sell=fake.random_int(min=60, max=150) * 100,
        date_buy=d_buy,
        date_expire=d_exp,
        amount=fake.random_int(min=1, max=100),
    )


def gen_payment(stock: PQueue) -> Payment:
    category: TypeUser = random.choice(USERS_CATEGORIES)
    course: TypeCourse = random.choice(COURSES_AVAILABLE)

    value_in_cents = random.randint(1000, 10000)

    return Payment(
        name=fake.name(),
        category=category,
        course=course,
        value=value_in_cents,
        items={
            stock.get_random_id(): fake.random_int(1, 100),
            stock.get_random_id(): fake.random_int(1, 100),
            stock.get_random_id(): fake.random_int(1, 100),
        },
        dttime=fake.date_time_between(start_date="-90d", end_date="+90d"),
    )

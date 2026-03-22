from faker import Faker
from datetime import timedelta
import random

from product import Product
from payment import COURSES_AVAILABLE, USERS_CATEGORIES, Payment, TypeUser, TypeCourse

fake = Faker()

# expiry_counter = 0


def gen_product() -> Product:
    # global expiry_counter
    # expiry_counter += 10

    d_buy = fake.date_between(start_date="-30d", end_date="today")
    d_exp = d_buy + timedelta(days=fake.random_int(min=1, max=100))

    # d_buy = date.today()
    # d_exp = d_buy + timedelta(days=expiry_counter)

    return Product(
        name=(
            fake.ecommerce_name()
            if hasattr(fake, "ecommerce_name")
            else fake.word().capitalize()
        ),
        price_buy=fake.random_int(min=5, max=50) * 100,
        price_sell=fake.random_int(min=60, max=150) * 100,
        date_buy=d_buy,
        date_expire=d_exp,
        amount=fake.random_int(min=1, max=100),
    )


def gen_payment() -> Payment:
    category: TypeUser = random.choice(USERS_CATEGORIES)
    course: TypeCourse = random.choice(COURSES_AVAILABLE)

    value_in_cents = random.randint(1000, 10000)

    return Payment(
        name=fake.name(),
        category=category,
        course=course,
        value=value_in_cents,
        items={0: 2, 1: 2, 2: 2},
        # dttime=fake.date_time_between(start_date='-30d', end_date='now')
    )

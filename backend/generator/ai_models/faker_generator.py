from faker import Faker 
import random

fake = Faker()

def generate_faker_value(field):
    
    if field.field_type == "string":
        return fake.name()
    elif field.field_type == "email":
        return fake.email()

    elif field.field_type == "number":
        return random.randint(18, 100000)

    elif field.field_type == "date":
        return fake.date()

    elif field.field_type == "boolean":
        return random.choice([True, False])

    elif field.field_type == "choice":
        return fake.word()

    return None
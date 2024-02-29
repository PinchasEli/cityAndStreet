import sys
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

from models.street import Street  # Import Street model
from settings.db import mongo_db


# Function to generate random street names
def generate_street_names(num_streets):
    street_suffixes = ["Street", "Avenue", "Lane", "Road", "Boulevard"]
    street_names = []
    for _ in range(num_streets):
        street_name = f"{random.choice(['First', 'Second', 'Third'])} {random.choice(['Main', 'Elm', 'Maple'])} {random.choice(street_suffixes)}"
        street_names.append(street_name)
    return street_names


# Function to create streets with random city IDs
async def create_random_streets(num_streets):
    city_ids = await mongo_db.city.distinct("_id")  # Retrieve list of city IDs
    street_names = generate_street_names(num_streets)  # Generate random street names
    random_streets = []
    for street_name in street_names:
        city_id = random.choice(city_ids)  # Assign random city ID
        street = Street(name=street_name, city=str(city_id))
        random_streets.append(street)
    await mongo_db.street.insert_many([street.dict() for street in random_streets])  # Insert streets into database


# Main function to execute the script
async def main():
    num_streets = 40  # Number of streets to generate
    await create_random_streets(num_streets)


# Run the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

from pymongo import MongoClient
from random import randint

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['FastAPI']  # Replace 'your_database_name' with your actual database name
collection = db['city']  # Assuming you have a 'city' collection

# List of city names in Israel
israeli_cities = [
    "Jerusalem", "Tel Aviv", "Haifa", "Rishon LeZion", "Petah Tikva",
    "Ashdod", "Netanya", "Beer Sheva", "Holon", "Bnei Brak",
    "Ramat Gan", "Herzliya", "Rehovot", "Ashkelon", "Bat Yam",
    "Kfar Saba", "Ra'anana", "Beit Shemesh", "Lod", "Nazareth",
    "Modi'in-Maccabim-Re'ut", "Hadera", "Kiryat Gat", "Hod HaSharon",
    "Kiryat Yam", "Nahariya", "Ramat HaSharon", "Lod", "Modi'in-Maccabim-Re'ut",
    "Qiryat Bialik", "Qiryat Yam", "Rosh HaAyin", "Safed", "Tiberias",
    "Yehud-Monosson", "Yavne", "Dimona", "Sderot", "Ness Ziona"
]

# Generate random population values (for demonstration, using randint)
# Adjust this as needed to reflect real population data
populations = [randint(50000, 1000000) for _ in range(40)]

# Create and insert city documents
for city_name, population in zip(israeli_cities, populations):
    city_doc = {
        "name": city_name,
        "population": population,
        "country": "Israel"
    }
    collection.insert_one(city_doc)

print("Cities inserted successfully.")

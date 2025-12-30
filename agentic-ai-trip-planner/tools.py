# tools.py
import random

def get_flights(origin, destination, dates):
    return [
        {"airline": "AirAI", "price": 400, "departure": dates[0], "arrival": dates[1]},
        {"airline": "SkyFly", "price": 350, "departure": dates[0], "arrival": dates[1]},
    ]

def get_hotels(city, nights, budget):
    return [
        {"name": "Hotel Lux", "price_per_night": 100, "rating": 4.5},
        {"name": "Budget Inn", "price_per_night": 60, "rating": 4.0},
    ]

def get_weather(city, dates):
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy"]
    return [{"date": d, "forecast": random.choice(conditions)} for d in dates]

def get_attractions(city):
    return ["Museum A", "Historic Site B", "Park C", "Local Market D"]

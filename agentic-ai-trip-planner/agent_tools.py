# agent_tools.py
from tools import get_flights, get_hotels, get_weather, get_attractions

# Use simple dict-based tool representations compatible with `create_react_agent`.
# Each tool is a dict with `name`, `func`, and `description`.
flight_tool = {
    # `name` must match ^[a-zA-Z0-9_-]+$ for OpenAI function/tool naming
    "name": "flight_planner",
    "display_name": "Flight Planner",
    "func": lambda args: str(get_flights(*args)),
    "description": "Use to find flight options. Input: origin, destination, dates",
}

hotel_tool = {
    "name": "hotel_finder
    "display_name": "Hotel Finder",
    "func": lambda args: str(get_hotels(*args)),
    "description": "Use to find hotels. Input: city, nights, budget",
}

weather_tool = {
    "name": "weather_checker",
    "display_name": "Weather Checker",
    "func": lambda args: str(get_weather(*args)),
    "description": "Use to get weather forecast. Input: city, dates",
}

attraction_tool = {
    "name": "attractions_finder",
    "display_name": "Attractions Finder",
    "func": lambda args: str(get_attractions(args)),
    "description": "Use to get list of attractions. Input: city",
}

tools = [flight_tool, hotel_tool, weather_tool, attraction_tool]


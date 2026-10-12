import requests

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52&longitude=13.41"
    "&current=temperature_2m,apparent_temperature,precipitation,wind_speed_10m"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    "&timezone=auto"
)

response = requests.get(URL, timeout=15)
response.raise_for_status()
data = response.json()

cur, today = data["current"], data["daily"]
print(f"Berlin now: {cur['temperature_2m']}°C (feels like {cur['apparent_temperature']}°C)")
print(f"Today: {today['temperature_2m_min'][0]}°C to {today['temperature_2m_max'][0]}°C, "
      f"rain chance {today['precipitation_probability_max'][0]}%")
print("Weather data by Open-Meteo.com")
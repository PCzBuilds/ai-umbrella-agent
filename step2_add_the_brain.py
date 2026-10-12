import os
import time
import requests

API_KEY = os.environ.get("MISTRAL_API_KEY")
if not API_KEY:
    raise SystemExit("MISTRAL_API_KEY is not set. Export it and rerun.")
MODEL = os.environ.get("MISTRAL_MODEL", "ministral-8b-latest")
TIMEOUT = 30

# Part A: fetch weather (same as Step 1)
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52&longitude=13.41"
    "&current=temperature_2m,apparent_temperature,precipitation,wind_speed_10m"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    "&timezone=auto"
)
resp = requests.get(WEATHER_URL, timeout=15)
resp.raise_for_status()
weather = resp.json()
cur, today = weather["current"], weather["daily"]
weather_summary = (
    f"City: Berlin\n"
    f"Current temperature: {cur['temperature_2m']}°C (feels like {cur['apparent_temperature']}°C)\n"
    f"Precipitation right now: {cur['precipitation']} mm\n"
    f"Wind speed: {cur['wind_speed_10m']} km/h\n"
    f"Today's high: {today['temperature_2m_max'][0]}°C, low: {today['temperature_2m_min'][0]}°C\n"
    f"Chance of rain today: {today['precipitation_probability_max'][0]}%"
)

# Part B: ask Mistral about it (a POST request: we're sending data now)
CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
payload = {
    "model": MODEL,
    "messages": [
        {"role": "system",
         "content": ("You are a friendly weather assistant. Use ONLY the data "
                     "provided. Answer in 2-3 short sentences and always give a "
                     "practical recommendation.")},
        {"role": "user",
         "content": f"Summarize today's weather for me.\n\n{weather_summary}"},
    ],
}
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# A 429 means "too many requests". The polite fix is waiting and retrying.
for attempt in range(1, 6):
    response = requests.post(CHAT_URL, json=payload, headers=headers, timeout=TIMEOUT)
    if response.status_code != 429:
        response.raise_for_status()
        break
    wait = 10 * attempt
    print(f"Rate limited (429). Waiting {wait}s before retrying...")
    time.sleep(wait)
else:
    raise SystemExit("Still rate limited after 5 tries. Try again later.")

print("Weather data fetched:\n" + weather_summary)
print("\nMistral says:\n" + response.json()["choices"][0]["message"]["content"])
print("\nWeather data by Open-Meteo.com")
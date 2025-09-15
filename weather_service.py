import requests
import time
from config import API_KEY, BASE_URL, CACHE_TTL
from utils import cache, normalize_city
from exceptions import RateLimitError

class GetWeather:
    def __init__(self):
        self.session = requests.Session()

    def _make_key(self, city: str, mode: str, extra: str = ""):
        city_norm = normalize_city(city)
        if extra:
            return f"{city_norm}:{mode}:{extra}"
        return f"{city_norm}:{mode}"

    def get_weather(self, city: str, use_cache: bool = True):
        key = self._make_key(city, "current")
        if use_cache:
            cached = cache.get(key)
            if cached:
                print(f"cache hit: {key}")
                return cached

        url = f"{BASE_URL}/weather"
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = self.session.get(url, params=params)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(retry_after=retry_after)

        response.raise_for_status()
        data = response.json()
        result = {
            "city": city,
            "temperature": f"{data['main']['temp']} degree celsius",
            "humidity": data['main'].get("humidity"),
            "sunrise": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['sys']['sunrise'])),
            "sunset": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['sys']['sunset'])),
        }

        if use_cache:
            cache.set(key, result, CACHE_TTL)
        return result

    def get_forecast(self, city: str, entries: int = 5, use_cache: bool = True):
        key = self._make_key(city, "forecast", extra=str(entries))
        if use_cache:
            cached = cache.get(key)
            if cached:
                print(f"cache hit: {key}")
                return cached

        url = f"{BASE_URL}/forecast"
        params = {"q": city, "appid": API_KEY, "units": "metric", "cnt": entries}
        response = self.session.get(url, params=params)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(retry_after=retry_after)

        response.raise_for_status()
        data = response.json()

        forecasts = []
        for entry in data.get("list"[:5])[:entries]:
            forecasts.append({
                "time": entry.get("dt_txt"),
                "description": entry.get("weather", [{}])[0].get("description"),
                "temperature": f"{entry['main']['temp']} degree celsius",
                "humidity": entry['main'].get("humidity"),
            })

        result = {
            "city": city,
              "forecast": forecasts
              }

        if use_cache:
            cache.set(key, result, CACHE_TTL)
        return result

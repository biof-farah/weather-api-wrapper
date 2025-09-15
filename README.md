# weather-api-wrapper

A simple Python project that fetches weather data from the [OpenWeather API](https://openweathermap.org/api) 

---

## Requirements

- Python 3.10+
- Python libraries listed in `requirements.txt`

---

##  Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/biof-farah/weather-api-wrapper.git
   cd weather-app
   - Create and activate a virtual environment in the next three steps (optional but recommended) -
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   create '.env' file containg: API_KEY='your_key' -> key from official [OpenWeather API] site
                                CACHE_TTL = 'value in second'
   python main.py
   Open your browser and try: http://localhost:8000/weather?city=London&mode=current
                              http://localhost:8000/weather?city=Paris&mode=forecast






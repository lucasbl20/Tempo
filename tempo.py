from flask import Flask, render_template
import requests
from datetime import datetime

# Sua chave API do OpenWeatherMap
API_KEY = "8da2a0c538b372e0bea06260337f29c9"
CITY = "Osasco, BR"
BASE_URL = ""

app = Flask(__name__)

def get_weather():
    try:
        params = {
            "q": CITY,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pt"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            return temperature, description, humidity, wind_speed
        else:
            return None
    except Exception as e:
        print(f"Erro ao buscar dados do tempo: {e}")
        return None

@app.route("/")
def home():
    weather = get_weather()
    if weather:
        temperature, description, humidity, wind_speed = weather

        # Obtendo o dia da semana e a data
        now = datetime.now()
        day_of_week = now.strftime('%A')  # Dia da semana em inglês
        current_date = now.strftime('%d/%m/%Y')  # Data no formato DD/MM/AAAA
        current_time = now.strftime('%H:%M:%S')  # Hora no formato HH:MM:SS

        # Traduzindo o dia da semana para português
        days_translation = {
            'Monday': 'Segunda-feira',
            'Tuesday': 'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira',
            'Friday': 'Sexta-feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        day_of_week = days_translation.get(day_of_week, day_of_week).capitalize()  # Traduz e capitaliza

        return render_template(
            "index.html",
            temperature=temperature,
            description=description,
            humidity=humidity,
            wind_speed=wind_speed,
            city=CITY,
            day_of_week=day_of_week,  # Dia da semana traduzido
            date=current_date,  # Data formatada
            time=current_time  # Hora inicial
        )
    else:
        return "<h1>Erro ao buscar dados do tempo. Tente novamente mais tarde.</h1>"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


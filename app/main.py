from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_advice(weather, temp):
    advice = []
    
    if weather == "Thunderstorm":
        advice.append("⚡ Stay home! Perfect time to watch these films before you die:")
        advice.append("🎬 <a href='https://www.imdb.com/list/ls055592025/' target='_blank'>IMDB Top 100 Must-Watch Films →</a>")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=epic+storm+playlist' target='_blank'>Epic Storm Playlist on YouTube Music →</a>")
    
    elif weather in ["Rain", "Drizzle"]:
        advice.append("☂️ Take an umbrella!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=rainy+day+playlist' target='_blank'>Rainy Day Playlist on YouTube Music →</a>")
    
    elif weather == "Snow":
        advice.append("🧤 Wear gloves and boots!")
        advice.append("🎬 Cozy night in — grab a blanket and watch something warm!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=cozy+winter+playlist' target='_blank'>Cozy Winter Playlist on YouTube Music →</a>")
    
    elif weather in ["Fog", "Mist"]:
        advice.append("🌫️ Drive carefully — low visibility today!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=chill+foggy+morning+playlist' target='_blank'>Chill Foggy Morning Playlist →</a>")
    
    elif weather == "Clear" and temp > 30:
        advice.append("🌡️ Dangerous heat! Stay in the shade and avoid going out if possible!")
        advice.append("🧢 Wear a hat — sun is intense!")
        advice.append("💧 Drink lots of water — stay hydrated!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=summer+hits+playlist' target='_blank'>Summer Hits Playlist on YouTube Music →</a>")

    elif weather == "Clear" and 25 <= temp <= 30:
        advice.append("🌡️ It's getting warm — wear a hat and stay hydrated! 🧢")
        advice.append("💧 Keep a water bottle with you!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=summer+vibes+playlist' target='_blank'>Summer Vibes Playlist on YouTube Music →</a>")

    elif weather == "Clear" and 15 <= temp < 25:
        advice.append("😎 What a beautiful day — be grateful for this moment! 🙏")
        advice.append("🌳 Go for a walk, touch some grass!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=happy+sunny+day+playlist' target='_blank'>Happy Sunny Day Playlist on YouTube Music →</a>")

    elif weather == "Clouds" and temp > 28:
        advice.append("🌡️ It's hot and cloudy — still apply sunscreen!")
        advice.append("💧 Stay hydrated!")
    
    elif temp < 11:
        advice.append("🥶 Winter is coming back! Layer up!")
        advice.append("🧥 Wear a heavy coat — it's freezing!")
        advice.append("☕ Hot coffee or tea time!")
    
    elif temp < 14:
        advice.append("🌬️ A bit chilly — maybe grab a light jacket just in case!")
        advice.append("☕ A warm drink wouldn't hurt!")
    
    else:
        advice.append("🌤️ Looks okay out there — have a great day!")
    
    return advice

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WeatherWise</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 50px 40px;
            width: 100%;
            max-width: 580px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        }
        h1 {
            color: white;
            font-size: 2.2rem;
            margin-bottom: 8px;
            text-align: center;
        }
        p.subtitle {
            color: rgba(255,255,255,0.6);
            text-align: center;
            margin-bottom: 30px;
            font-size: 1rem;
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        input {
            flex: 1;
            padding: 14px 18px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 16px;
            outline: none;
        }
        input::placeholder { color: rgba(255,255,255,0.4); }
        input:focus { border-color: #e94560; }
        button {
            padding: 14px 24px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #e94560, #0f3460);
            color: white;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: opacity 0.2s;
        }
        button:hover { opacity: 0.85; }
        .result {
            background: rgba(255,255,255,0.07);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .result h2 {
            color: white;
            font-size: 1.6rem;
            margin-bottom: 8px;
        }
        .meta {
            color: rgba(255,255,255,0.6);
            margin-bottom: 16px;
            font-size: 0.95rem;
        }
        hr { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 16px 0; }
        .advice {
            color: white;
            font-size: 1.05rem;
            margin: 10px 0;
            line-height: 1.6;
        }
        .advice a { color: #e94560; text-decoration: none; }
        .advice a:hover { text-decoration: underline; }
        .error { color: #e94560; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 WeatherWise</h1>
        <p class="subtitle">Enter a city to get weather-based recommendations</p>
        <form method="GET" action="/weather">
            <div class="search-box">
                <input type="text" name="city" placeholder="e.g. New York, Istanbul, Tokyo" value="{{ city }}">
                <button type="submit">Check</button>
            </div>
        </form>
        {% if result %}
        <div class="result">
            <h2>{{ result.city }}, {{ result.country }}</h2>
            <div class="meta">
                🌡️ {{ result.temp }}°C &nbsp;|&nbsp; 🌤️ {{ result.condition }}
            </div>
            <hr>
            {% for a in result.advice %}
            <p class="advice">{{ a | safe }}</p>
            {% endfor %}
        </div>
        {% endif %}
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, result=None, error=None, city="")

@app.route("/weather")
def weather():
    city = request.args.get("city", "")
    if not city:
        return render_template_string(HTML, result=None, error="Please enter a city name.", city="")
    
    response = requests.get(BASE_URL, params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    })
    
    if response.status_code != 200:
        return render_template_string(HTML, result=None, error=f"City '{city}' not found.", city=city)
    
    data = response.json()
    condition = data["weather"][0]["main"]
    temp = round(data["main"]["temp"])
    country = data["sys"]["country"]
    
    result = {
        "city": data["name"],
        "country": country,
        "temp": temp,
        "condition": condition,
        "advice": get_advice(condition, temp)
    }
    
    return render_template_string(HTML, result=result, error=None, city=city)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
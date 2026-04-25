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
        advice.append("☀️ Apply sunscreen! It's hot out there!")
        advice.append("💧 Stay hydrated — drink plenty of water!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=summer+hits+playlist' target='_blank'>Summer Hits Playlist on YouTube Music →</a>")
    
    elif weather == "Clear" and 15 <= temp <= 30:
        advice.append("😎 What a beautiful day — be grateful for this moment! 🙏")
        advice.append("🌳 Go for a walk, touch some grass!")
        advice.append("🎵 <a href='https://music.youtube.com/search?q=happy+sunny+day+playlist' target='_blank'>Happy Sunny Day Playlist on YouTube Music →</a>")
    
    elif temp < 5:
        advice.append("🧥 Wear a heavy coat — it's freezing!")
        advice.append("☕ Hot coffee or tea time!")
    
    else:
        advice.append("🌤️ Looks okay out there — have a great day!")
    
    return advice

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WeatherWise</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        input { padding: 10px; width: 70%; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background: #0077cc; color: white; border: none; cursor: pointer; }
        .result { margin-top: 30px; padding: 20px; background: #f0f8ff; border-radius: 8px; }
        .advice { font-size: 18px; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>🌍 WeatherWise</h1>
    <p>Enter a city to get weather-based recommendations</p>
    <form method="GET" action="/weather">
        <input type="text" name="city" placeholder="e.g. New York, Istanbul, Tokyo" value="{{ city }}">
        <button type="submit">Check</button>
    </form>
    {% if result %}
    <div class="result">
        <h2>{{ result.city }}, {{ result.country }}</h2>
        <p>🌡️ Temperature: {{ result.temp }}°C</p>
        <p>🌤️ Condition: {{ result.condition }}</p>
        <hr>
        {% for a in result.advice %}
        <p class="advice">{{ a }}</p>
        {% endfor %}
    </div>
    {% endif %}
    {% if error %}
    <p style="color:red">{{ error }}</p>
    {% endif %}
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
from flask import Flask, render_template, request   # FIXED 2: removed "app" from the import
from weather import get_current_weather, get_local_time
from waitress import serve

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Handle an empty search (FIXED A)
    if not bool(city.strip()):
        city = "Abuja"

    weather_data = get_current_weather(city)
        
    print("DEBUG weather_data:", weather_data)   # temporary

    # FIXED B: if the API says "not found", show a friendly page instead of crashing
    if weather_data is None:
        return render_template("city-not-found.html", message="Could not reach the weather service. Check your connection.")

    if str(weather_data.get("cod")) != "200":
        return render_template("city-not-found.html", message="Sorry, we couldn't find that city.")
    
    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]
    local_time = get_local_time(lat, lon) or "Unable to fetch local time"  # FIXED C: if the API fails, show "Unavailable" instead of crashing

    return render_template(
        "weather.html",
        title=weather_data["name"],
       #  feels_like=f"{weather_data['main']['feels_like']:.1f}",
        local_time=local_time,
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
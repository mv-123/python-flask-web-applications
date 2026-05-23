from flask import Flask, request, render_template
from datetime import datetime
import urllib.request, json

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def weather():
    if request.method == "POST":
        city = request.form["city"]
    else:
        city = 'Frisco'
    
    api = "3e3a4caf78664bca1735e30e9ead6ffa"
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api + '&units=imperial').read()
    weather_data = json.loads(source)
    print(weather_data)

    sunrise = weather_data["sys"]["sunrise"]
    sunset = weather_data["sys"]["sunset"]
    converted_sunrise = datetime.fromtimestamp(sunrise).strftime("%H:%M:%S")
    converted_sunset = datetime.fromtimestamp(sunset).strftime("%H:%M:%S")

    dictionary = {"country_code": weather_data["sys"]["country"], "coordinates": str(weather_data["coord"]["lon"]) + ", " + str(weather_data["coord"]["lon"]), "temperature": weather_data["main"]["temp"], "sunrise": converted_sunrise, "sunset": converted_sunset}
    print(dictionary)

    return render_template("index.html", data = dictionary)
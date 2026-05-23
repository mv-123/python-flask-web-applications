from flask import Flask, request, render_template
import urllib.request, json

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def countries():
    if request.method == "POST":
        country = request.form["country"]
    else:
        country = 'india'
    
    source = urllib.request.urlopen('https://restcountries.com/v3.1/name/' + country).read()
    country_data = json.loads(source)
    print(country_data)

    c = country_data[0]
    result = {"name": c.get("name", {}).get("common", "N/A"),
              "capital": c.get("capital", "N/A")[0],
              "population": c.get("population", "N/A")}

    return render_template("index.html", country = result)
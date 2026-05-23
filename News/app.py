from flask import Flask, request, render_template
import urllib.request, json

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def news():
    if request.method == "POST":
        topic = request.form["topic"]
    else:
        topic = 'food'
    
    api = "18c8ff77f7184c52a8433e6b75eba9d9"
    source = urllib.request.urlopen('https://newsapi.org/v2/everything?q=' + topic + '&apiKey=' + api).read()
    news_data = json.loads(source)
    print(news_data)

    articles = news_data.get("articles")

    return render_template("index.html", articles = articles, topic = topic)
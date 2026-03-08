import requests
from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

API_KEY = "DEMO_KEY"
BASE_URL = "https://api.nasa.gov/planetary/apod"


@app.route("/", methods=["GET", "POST"])
def main():

    selected_date = date.today().strftime("%Y-%m-%d")

    if request.method == "POST":
        selected_date = request.form.get("date")

    params = {
        "api_key": API_KEY,
        "date": selected_date
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        nasa_data = response.json()
        return render_template("index.html", data=nasa_data)
    else:
        return render_template("index.html", data=None)


if __name__ == "__main__":
    app.run(debug=True)
import requests
from flask import Flask, render_template

app = Flask(__name__)

# Your NASA API key
api_key = "8yh3fbmSIRV0m1JYfBLAdVfsHD9UqdvB8PbzxBh5"
url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"


@app.route("/")
def main():
    response = requests.get(url)
    if response.status_code == 200:
        nasa_data = response.json()
        return render_template("index.html", data=nasa_data)
    return "Error fetching NASA data"


@app.route("/<date>")
def specific_date(date):
    # date format: YYYY-MM-DD
    response = requests.get(url + "&date=" + date)
    if response.status_code == 200:
        nasa_data = response.json()
        return render_template("index.html", data=nasa_data)
    return "Invalid date or API error"


@app.route("/apikey")
def show_apikey_page():
    return render_template("apikey.html")


if __name__ == "__main__":
    app.run(debug=True)

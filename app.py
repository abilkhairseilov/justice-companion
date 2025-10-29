from flask import Flask, render_template, jsonify, request
import src.backend
import pandas as pd


app = Flask(__name__)

df = pd.read_csv("data/countries.csv")
countries = df["name"].tolist()
country_data = df.set_index("name")[["gdp_pcap", "co2_pcap", "child_mort_pcap"]].to_dict(orient="index")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", countries = countries, country_data = country_data)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    gdp = data.get("gdp")
    co2 = data.get("co2")
    mortality = data.get("mortality")

    lex = src.backend.predict_lex(gdp, co2, mortality)
    return jsonify({"prediction": round(lex, 1)})

@app.route("/facts")
def facts():
    return render_template("facts.html")

@app.route("/about")
def about():
    return render_template("about.html")
if __name__ == "__main__":
    app.run(debug=True)

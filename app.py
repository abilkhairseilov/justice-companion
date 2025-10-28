from flask import Flask, render_template, jsonify, request
import src.backend

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    gdp = data.get("gdp")
    co2 = data.get("co2")
    mortality = data.get("mortality")

    lex = src.backend.predict_lex(gdp, co2, mortality)
    return jsonify({"prediction": round(lex, 1)})

if __name__ == "__main__":
    app.run(debug=True)

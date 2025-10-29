import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
import joblib



def predict_lex(gdp, co2, mortality):
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)


    w1 = model["w1"]
    b1 = model["b1"]
    w2 = model["w2"]
    b2 = model["b2"]
    gdp = float(gdp)
    co2 = float(co2)
    mortality = float(mortality)
    x = np.array([[gdp, co2, mortality]])
    with open("models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    x_scaled = scaler.transform(x)
    z1 = x_scaled @ w1 + b1
    a1 = np.maximum(0, z1)
    y_pred = a1 @ w2 + b2
    return float(y_pred.squeeze())

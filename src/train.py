import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

dataset = pd.read_csv("data/dataset_preprocessed.csv")
gdp_pcap = dataset['gdp_pcap']
co2_pcap = dataset['co2_pcap']
child_mort_pcap = dataset['child_mort_pcap']

X = dataset[['gdp_pcap', 'co2_pcap', 'child_mort_pcap']].values
y = dataset['lex'].values

# start weight and bias initializationw

lr = 0.01

# 3 inputs, 4 hidden neurons
w1 = np.random.randn(3, 4) * 0.01
b1 = np.zeros(4)

# 4 inputs, 1 output neuron
w2 = np.random.randn(4, 1) * 0.01
b2 = np.zeros(1)

# forward propagation
z1 = X @ w1 + b1
a1 = np.maximum(0, z1)

y_pred = a1 @ w2 + b2

# backwards propagation
# derivative of loss with respect to predicted y
# loss = np.mean((y_pred.squeeze() - y) ** 2)

dL_dy_pred = 2 * (y_pred.squeeze() - y) / len(y)  # pyright: ignore[reportUnknownVariableType, reportOperatorIssue]

dL_dw2 = a1.T @ dL_dy_pred.reshape(-1,1)
dL_db2 = np.sum(dL_dy_pred)

da1 = dL_dy_pred.reshape(-1,1) @ w2.T
dz1 = da1 * (z1 > 0).astype(float)
dL_dw1 = X.T @ dz1
dL_db1 = np.sum(dz1, axis=0)

w1 -= lr * dL_dw1
b1 -= lr * dL_db1
w2 -= lr * dL_dw2
b2 -= lr * dL_db2

# print(loss)
# print("PREDICTED Y")
# print(y_pred)

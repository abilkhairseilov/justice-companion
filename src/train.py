import numpy as np
import pandas as pd

dataset = pd.read_csv("data/dataset_preprocessed.csv")

X = dataset[["gdp_pcap", "co2_pcap", "child_mort_pcap"]].values
y = dataset["lex"].values

# start weight and bias initializationw
# 3 inputs, 4 hidden neurons
w1 = np.random.randn(3, 4) * 0.01
b1 = np.zeros(4)

# 4 inputs, 1 output neuron
w2 = np.random.randn(4, 1) * 0.01
b2 = np.zeros(1)

lr = 0.01
epochs = 1000
for epoch in range(epochs):
    # forward propagation
    z1 = X @ w1 + b1
    a1 = np.maximum(0, z1)

    y_pred = a1 @ w2 + b2

    # backwards propagation
    # derivative of loss with respect to predicted y
    loss = np.mean((y_pred.squeeze() - y) ** 2)

    dL_dy_pred = 2 * (y_pred.squeeze() - y) / len(y)  # pyright: ignore[reportUnknownVariableType, reportOperatorIssue]

    dL_dw2 = a1.T @ dL_dy_pred.reshape(-1, 1)
    dL_db2 = np.sum(dL_dy_pred)

    da1 = dL_dy_pred.reshape(-1, 1) @ w2.T
    dz1 = da1 * (z1 > 0).astype(float)
    dL_dw1 = X.T @ dz1
    dL_db1 = np.sum(dz1, axis=0)

    w1 -= lr * dL_dw1
    b1 -= lr * dL_db1
    w2 -= lr * dL_dw2
    b2 -= lr * dL_db2

    # if epoch % 100 == 0:
    #     print(f"epoch: {epoch}\nloss: {loss}")


# training done
# print(loss)
# print("PREDICTED Y")
# print(f"epoch: {epoch}\nloss: {loss}")
# print(y_pred)


# actual prediction
# we can try predicting with actual values of a country, inputting them to the MLP and comparing results with the actual lex
# qatar has:
# 0.15619315758173222, 0.15925531524253664, 0.04098349977481082, 77.31

qatar = np.array([0.15619315758173222, 0.15925531524253664, 0.04098349977481082])

z1 = qatar @ w1 + b1
a1 = np.maximum(0, z1)
y_pred = a1 @ w2 + b2


print(f"y_pred: {y_pred}, actual lex: 77.31")

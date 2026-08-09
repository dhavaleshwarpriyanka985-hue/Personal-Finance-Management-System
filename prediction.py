import pandas as pd
from sklearn.linear_model import LinearRegression

# Example monthly data
data = {
    "Month": [1, 2, 3, 4, 5, 6],
    "Expense": [15000, 16500, 18000, 17000, 19000, 20000]
}

df = pd.DataFrame(data)

X = df[["Month"]]
y = df["Expense"]

model = LinearRegression()
model.fit(X, y)

next_month = [[7]]

prediction = model.predict(next_month)

print("Predicted Expense:", prediction[0])


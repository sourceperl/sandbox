"""
Linear Regression from Scratch with Gradient Descent

This module implements a univariate linear regression model using NumPy. 
It demonstrates the mathematical foundations of machine learning, including:
- Hypothesis function (Matrix multiplication)
- Mean Squared Error (MSE) Cost Function
- Batch Gradient Descent optimization
- Coefficient of Determination (R²) evaluation

The script generates a synthetic dataset, trains the model, and visualizes 
both the resulting regression line and the cost convergence over time.
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_regression


def model_predict(X: np.ndarray, theta: np.ndarray) -> np.ndarray:
    return X.dot(theta)


def cost_func(X: np.ndarray, y: np.ndarray, theta: np.ndarray) -> float:
    m = y.size
    errors = model_predict(X, theta) - y
    return (1 / (2 * m)) * np.sum(errors**2)


def gradient_descent(X: np.ndarray, y: np.ndarray, theta: np.ndarray,
                     learning_rate: float, n_iterations: int):
    m = y.size
    cost_history = np.zeros(n_iterations)

    for i in range(n_iterations):
        # adjust theta at each iteration
        y_predict = model_predict(X, theta)
        predict_error = y_predict - y
        gradient = (1 / m) * (X.T.dot(predict_error))
        theta -= learning_rate * gradient
        cost_history[i] = cost_func(X, y, theta)

    return theta, cost_history


def r2_score(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = np.sum((y - pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1 - (ss_res / ss_tot)


# build dataset
x, y, coefs = make_regression(n_samples=100, n_features=1, noise=10, bias=50, coef=True, random_state=42)
y = y.reshape(-1, 1)

# add bias term (column of ones)
X = np.c_[x, np.ones(x.shape[0])]

# parameters
N_ITERATIONS = 1_000
LEARNING_RATE = 0.01
theta_init = np.array([[0.0], [0.0]])

# training
theta_final, cost_history = gradient_descent(X, y, theta_init, LEARNING_RATE, N_ITERATIONS)
predictions = model_predict(X, theta_final)
score = r2_score(y, predictions)

# visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# regression line
ax1.set_title(f'Linear Regression (R² = {score:.3f})')
ax1.scatter(x, y, alpha=0.6, label='Data')
ax1.plot(x, predictions, color='red', linewidth=2, label='Prediction')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# cost history (learning curve)
ax2.set_title('Cost Function History (Convergence)')
ax2.plot(cost_history, color='blue')
ax2.set_xlabel('Iterations')
ax2.set_ylabel('MSE Cost')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

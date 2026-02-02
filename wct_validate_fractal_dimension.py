# WCT Validation: Fractal Dimension (asymptotic fit)

import numpy as np
import matplotlib.pyplot as plt

# Parameters
r = 0.5646
beta = 3.95
gamma = 0.05
xi_0 = 1e-5
N = 200

n = np.arange(1, N + 1)

xi_n = xi_0 * r**n
E_n = r**(beta * n) * np.exp(-gamma * n)

# Log variables
X = np.log(xi_n)
Y = np.log(E_n)

# Linear fit over tail
fit_start = int(0.3 * N)
slope, intercept = np.polyfit(X[fit_start:], Y[fit_start:], 1)

D_f = slope

print("Asymptotic fractal dimension D_f =", D_f)

# Plot
plt.plot(X, Y, '.', label='data')
plt.plot(X, slope * X + intercept, '-', label='fit')
plt.xlabel("log xi")
plt.ylabel("log E")
plt.legend()
plt.grid(True)
plt.show()

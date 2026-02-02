
import numpy as np
import matplotlib.pyplot as plt

# Parameters
r = 0.5646
beta = 3.95
gamma = 0.05
xi_0 = 1e-5
N = 120
n = np.arange(1, N + 1)

# Recursive quantities
xi_n = xi_0 * r**n
E_n = r**(beta * n) * np.exp(-gamma * n)

# Compute fractal dimension D_f
log_E = np.log(E_n)
log_xi_inv = np.log(1 / xi_n)
D_f = -log_E / log_xi_inv

# Plot
plt.figure(figsize=(8, 5))
plt.plot(n, D_f, label="Fractal Dimension D_f(n)")
plt.xlabel("Shell Index n")
plt.ylabel("Fractal Dimension D_f")
plt.title("Fractal Dimension from Recursive Curvature Suppression")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("fractal_dimension_plot.png")
plt.show()

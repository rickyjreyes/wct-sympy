
import numpy as np
import matplotlib.pyplot as plt

# Parameters
r = 0.5646
beta = 3.95
gamma = 0.05
N = 120
n = np.arange(N + 1)
E_n = r**(beta * n) * np.exp(-gamma * n)
a_n = np.exp(np.cumsum(E_n))  # Expansion factor

plt.figure(figsize=(10, 5))
plt.plot(n, a_n)
plt.xlabel("Shell index n")
plt.ylabel("Expansion factor a(n)")
plt.title("Recursive Expansion Function a(n) from Cumulative Energy")
plt.grid(True)
plt.tight_layout()
plt.savefig("recursive_expansion_plot.png")
plt.show()

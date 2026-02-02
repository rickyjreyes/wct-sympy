
import numpy as np
import matplotlib.pyplot as plt

r = 0.5646
beta = 3.95
gamma = 0.05
dt = 1e-43  # Planck time spacing
n = np.arange(121)
t_n = n * dt
E_n = r**(beta * n) * np.exp(-gamma * n)
a_n = np.exp(np.cumsum(E_n))

H_n = np.gradient(np.log(a_n), t_n)  # Hubble-like parameter

plt.plot(t_n[1:], H_n[1:])
plt.xlabel("Time (s)")
plt.ylabel("Effective H(t)")
plt.title("Effective Hubble Parameter from Recursive Expansion")
plt.grid(True)
plt.tight_layout()
plt.savefig("hubble_parameter_from_shells.png")
plt.show()

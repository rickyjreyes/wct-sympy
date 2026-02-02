
import numpy as np
import matplotlib.pyplot as plt

# Parameters
r = 0.5646
beta_values = [2, 3, 4, 5]
gamma = 0.05
N_max = 120
n = np.arange(0, N_max + 1)

plt.figure(figsize=(10, 6))

# Plot suppression curves for each beta
for beta in beta_values:
    suppression = r**(beta * n) * np.exp(-gamma * n)
    label = f'beta={beta}, gamma={gamma}'
    plt.plot(n, suppression, label=label)

plt.yscale('log')
plt.xlabel('Shell index n')
plt.ylabel('Suppression factor E_n')
plt.title('Recursive Suppression with Beta and Entropy Feedback')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("recursive_suppression_plot.png")
plt.show()

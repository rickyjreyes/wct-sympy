
# Estimate minimum black hole mass from confinement scale
c = 2.998e8       # Speed of light in m/s
G = 6.67430e-11   # Gravitational constant in m^3/kg/s^2
xi = 10e-6        # Coherence length in meters (10 microns)

M_min = (c**2 * xi) / G
print(f"Minimum black hole mass from WCT: {M_min:.2e} kg")

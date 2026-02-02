import sympy as sp

# Symbol
x = sp.symbols('x', real=True)

# Curvature and density
W = sp.Function('W')(x)
rho = sp.Function('rho')(x)

# Mass parameter
m = sp.symbols('m', positive=True)
kappa = sp.symbols('kappa', positive=True)

# Mass–curvature relation
mass_curvature_law = sp.Eq(m, kappa * sp.integrate(W, x))

# Solenoidal mass condition (1D divergence-free)
J_m = sp.Function('J_m')(x)
solenoidal_mass = sp.Eq(sp.diff(J_m, x), 0)

# Density-weighted locking
density_weighted_locking = sp.Eq(m, sp.integrate(rho * W, x))

# -----------------------------
# PRINT RESULTS
# -----------------------------
print("\nTier 2: Mass–Curvature Relations (Internal Consequences)\n")

print("Mass–curvature law:")
sp.pprint(mass_curvature_law, use_unicode=False)

print("\nSolenoidal mass condition:")
sp.pprint(solenoidal_mass, use_unicode=False)

print("\nDensity-weighted locking:")
sp.pprint(density_weighted_locking, use_unicode=False)

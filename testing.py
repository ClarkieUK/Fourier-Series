import scipy.integrate as integrate
import sympy as sp

x = sp.symbols('x')
n = sp.symbols('n')
f = (1/sp.pi) * 1/3 * x**3 * sp.sin(n*x)

lower = -sp.pi
upper = sp.pi

integral = sp.integrate(f,(x,lower,upper))
simplified_integral = sp.simplify(integral)
print(simplified_integral)

from sympy import *

t = symbols('t', real=True)
expr = sin(t)+2*cos(t)  # unknown

d = collect(expr.expand(trig=True), [sin(t), cos(t)], evaluate=False)
a = d[sin(t)]
b = d[cos(t)]

cos_phase = atan(a/b)
amplitude = a / sin(cos_phase)
print(amplitude.evalf() * cos(t - cos_phase.evalf()))
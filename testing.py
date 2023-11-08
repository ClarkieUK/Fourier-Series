LIMIT = 5
SCALE = 80
LIMIT = 100

import numpy as np

for n in range(1,100) :
    
    cos_coeffs = []
    sin_coeffs = []
    cos_frequencies = []
    sin_frequencies = []
    
    cos_frequencies.append(360*2*n)
    
    sin_frequencies.append(360*n)
    cos_coeffs.append(SCALE * 1/(4*n**2-1))
    sin_coeffs.append(SCALE * 1/n)
    
    data = [sin_coeffs,sin_frequencies],[cos_coeffs,cos_frequencies],[[0]*LIMIT,[np.pi/2]*LIMIT]
    
    
import numpy as np
p = np.array([150 * 10**9 * (2**0.5), 150 * 10**9 * (2**0.5)])
sun = np.array([150,150])
G = 6.674 * 10**-11
# Berechnung des Beschleunigungsvektors
def Acc (msun, G, sun, b):
    return G * ((msun * b) / (np.linalg.norm(sun - b) * np.linalg.norm(sun - b)))
print(Acc(10**30, G, sun, p))

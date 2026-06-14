import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def modelo(x,t):
    C = x[0]
    # Parâmetros:
    V = 15 # m²
    F1 = 1 # m³ / s
    F2 = 1 # m³ / s
    F = 2 # m³ / s
    C1 = 1 # mol / m³
    C2 = 1 # mol / m³
    # E.D.O.'s:
    dCdt = ((F1 * C1) + (F2 * C2) - (F * C)) / V
    return [dCdt]

# Condições Iniciais
C0 = 0 # mol / m³

# Intervalo de Tempo
t = np.linspace(0, 60)

y = odeint(modelo,[C0],t)
C = y[:, 0]

data = np.vstack((t, C.T))
data = data.T
np.savetxt('data.txt', data, delimiter=',')

# Plotando os Gráficos:

x = t
y = C
plt.figure()
plt.xlabel('Tempo(Dias)')
plt.ylabel('C(mol / m³)')
plt.plot(x, y, label='Concentração')
plt.legend()
plt.show()

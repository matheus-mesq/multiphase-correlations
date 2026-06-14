import correlações_energia
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def calc_coef():
    my_params = correlações_energia.Parametros_entrada()
    U = correlações_energia.calc_U(my_params)
    print(U)

def calc_fluxo():
    my_params = correlações_energia.Parametros_entrada()
    U = correlações_energia.calc_U(my_params)
    Qf = correlações_energia.calc_Qf(U, my_params)
    print(Qf)

def calc_per():
    my_params = correlações_energia.Parametros_entrada()
    Sp = correlações_energia.calc_Sp(my_params)
    print(Sp)

def calc_grad_ent():
    my_params = correlações_energia.Parametros_entrada()
    U = correlações_energia.calc_U(my_params)
    Sp = correlações_energia.calc_Sp(my_params)
    Qf = correlações_energia.calc_Qf(U, my_params)
    dHdL = correlações_energia.calc_dHdL(Sp, Qf, my_params)
    print(dHdL)

def calc_ent():
    my_params = correlações_energia.Parametros_entrada()
    H_m_agua = correlações_energia.calc_H_m_agua(my_params)
    H_m_gas = correlações_energia.calc_H_m_gas(my_params)
    H_e = correlações_energia.calc_H_e(H_m_agua, H_m_gas, my_params)
    print(H_e)

def modelo(x, L):
    H = x[0]

    # E.D.O.:

    my_params = correlações_energia.Parametros_entrada()

    U = correlações_energia.calc_U(my_params)
    Sp = correlações_energia.calc_Sp(my_params)
    Qf = correlações_energia.calc_Qf(U, my_params)

    dHdL = correlações_energia.calc_dHdL(Sp, Qf, my_params)
    return [dHdL]

# Condições iniciais:

H0 = 20 # J / kg

L = np.linspace(0, 15)

y = odeint(modelo,[H0],L)
H = y[:, 0]

data = np.vstack((L, H.T))
data = data.T

# Plotando o Gráfico:

x = L
y = H
plt.figure()
plt.xlabel('Comprimento(m)')
plt.ylabel('Entalpia Específica(J/kg)')
plt.plot(x, y)

if __name__ == '__main__':

    # calc_coef()

    # calc_fluxo()

    # calc_per()

    # calc_grad_ent()

    calc_ent()

    # plt.show()

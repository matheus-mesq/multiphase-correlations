import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import multiphase_equations

def modelo(x,L):
    P = x[0]

    # E.D.O.:

    my_params = multiphase_equations.PhysicalChemicalProperties()

    dg = multiphase_equations.calc_dg(my_params)
    mil = multiphase_equations.calc_mil(my_params)
    mig = multiphase_equations.calc_mig(dg, my_params)
    Ap = multiphase_equations.calc_Ap(my_params)
    vsl = multiphase_equations.calc_vsl(Ap, my_params)
    vsg = multiphase_equations.calc_vsg(Ap, my_params)
    vm = multiphase_equations.calc_vm(vsl, vsg)
    Cl = multiphase_equations.calc_Cl(my_params)
    _min = multiphase_equations.calc_min(mil, mig, Cl)
    dn = multiphase_equations.calc_dn(dg, Cl, my_params)
    Hl = multiphase_equations.fun_Hl(my_params)
    dtp = multiphase_equations.calc_dtp(dg, Hl, my_params)
    dPedL = multiphase_equations.calc_dPedL(dtp, my_params)
    y = multiphase_equations.calc_y(Cl, Hl)
    S = multiphase_equations.calc_S(y)
    Re = multiphase_equations.calc_Re(dn, vm, _min, my_params)
    fn = multiphase_equations.calc_fn(Re, my_params)
    ftp = multiphase_equations.calc_ftp(fn, S)
    dPadL = multiphase_equations.calc_dPadL(ftp, dn, vm, my_params)

    dPdL = - (dPadL + dPedL) / (1 - (dtp * vm * vsg / P))
    return [dPdL]

# Condições Iniciais

P0 = multiphase_equations.PhysicalChemicalProperties().P0

L = np.linspace(0, 15.24)

y = odeint(modelo,[P0],L)
P = y[:, 0]

data = np.vstack((L, P.T))
data = data.T

# Plotando o Gráfico:

x = L
y = P
plt.figure()
plt.xlabel('Comprimento(m)')
plt.ylabel('Pressão(Pa)')
plt.plot(x, y)
plt.show()

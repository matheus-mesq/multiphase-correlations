import numpy as np
import matplotlib.pyplot as plt
import multiphase_equations

def create_my_parameters_reference(table_row):

    ql = multiphase_equations.PhysicalChemicalProperties().ql

    beta = table_row['beta']

    ang = table_row['ang']

    pipe_length = multiphase_equations.PhysicalChemicalProperties().L
    pp = multiphase_equations.PhysicalChemicalProperties(

        qg=(beta * ql) / (1 - beta),

        ang=ang

    )

    calculator_bb = multiphase_equations.BeggAndBrillCalculator(pp)
    dPdL = - calculator_bb.calculate_dPdL()

    dP = dPdL * pipe_length

    return dP

npts = 100
beta = np.linspace(0, 0.9, npts)
ang = np.linspace(-np.pi/2, np.pi/2, npts)
XX, YY = np.meshgrid(beta, ang)
ZZ_deltap = np.empty_like(XX)
for i in range(XX.shape[0]):
    for j in range(XX.shape[1]):
        beta = XX[i,j]
        ang = YY[i,j]
        table_row = {'beta': beta, 'ang': ang}
        ZZ_deltap[i,j] = create_my_parameters_reference(table_row)
plt.rcParams['font.size'] = 15
plt.pcolormesh(XX, 57.2958 * YY, ZZ_deltap * 1e-5)
plt.colorbar(label = 'dP(bar)')
plt.xlabel('Fração volumétrica de gás')
plt.ylabel('Ângulo de inclinação do duto(°)')
plt.show()

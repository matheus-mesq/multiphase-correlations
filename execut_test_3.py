import multiphase_equations_3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint

SECTIONS_INFO = [
        {'case': 1, 'params_sections': [{'length': 15.24, 'elevation': 1.12, 'angle': 0.07}]},
        {'case': 2, 'params_sections': [{'length': 15.24, 'elevation': -1.14, 'angle': -0.08}]},
        {'case': 3, 'params_sections': [{'length': 15.24, 'elevation': 1.86, 'angle': 0.12}]},
        {'case': 4, 'params_sections': [{'length': 15.24, 'elevation': -1.01, 'angle': -0.07}]},
        {'case': 5, 'params_sections': [
            {'length': 30.48, 'elevation': 0.07, 'angle': -0.002},
            {'length': 14.02, 'elevation': 2.01, 'angle': 0.14}
        ]},
        {'case': 6, 'params_sections': [{'length': 16.46, 'elevation': -1.69, 'angle': -0.1}]},
    ]

def create_my_parameters_reference(table_row):

    P = table_row['P']
    T = table_row['T']
    F = table_row['F']
    Fgas = table_row['Fgas']

    return multiphase_equations_3.PhysicalChemicalProperties(
        ql=F,
        qg=Fgas,
        D=0.052,
        e = 0,
        dl=999.55,
        ts=0.06,
        MG = 0.016,
        g=9.8,
        ang=0.07,
        z=1.12,
        L=15.24,
        T=T,
        P0=P
    )

def funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD):

    P = P_psia * 6894.76

    T = ((T_F - 32) * 5 / 9) + 273.15

    F = F_BD * 1.589873 * (10 ** - 1) / (24 * 3600)

    Fgas = Fgas_scfD * 2.863640 * (10 ** - 2) * 351.82 * T / (24 * 3600 * P)

    return P, T, F, Fgas

def calc_dP_sections_single_row(table_row, SECTIONS_INFO, expected_Pdrop=None, print_calcs=False):
    npts = len(SECTIONS_INFO)
    dP_calcs = np.empty(len(SECTIONS_INFO))
    for i in range(npts):
        row = SECTIONS_INFO[i]
        dP_tot = 0.0
        for j in range(len(row['params_sections'])):
            parms_dict = row['params_sections'][j]
            length = parms_dict['length']
            elevation = parms_dict['elevation']
            angle = parms_dict['angle']
            my_params_iteration = create_my_parameters_reference(
                table_row
            )
            my_params_iteration.L = length
            my_params_iteration.z = elevation
            my_params_iteration.ang = angle
            L = length
            calculator_bb = multiphase_equations_3.BeggAndBrillCalculator(my_params_iteration)
            dPdL = calculator_bb.calculate_dPdL()
            dP = dPdL * L
            dP_tot = dP_tot + dP
        if print_calcs:
            error_perc = 100.0*(expected_Pdrop[i] - dP_tot) / expected_Pdrop[i]
            print('[{}] Calculated dPf Section {} = {:.2f} (expected = {:.2f}; {:.2f}%)'.format(
                'asc' if angle > 0 else 'desc',
                i+1, dP_tot, expected_Pdrop[i], error_perc)
            )
        dP_calcs[i] = dP_tot
    return dP_calcs

def main_calc_dPf_with_the_class_single_row():

    print('Delta P for Payne row 12202:')

    df_raw = pd.read_csv("payne-Pdrop.csv")

    row = df_raw.loc[2]
    P_psia = row["P[psia]"]
    T_F = row["T[F]"]
    F_BD = row["F[B/D]"]
    Fgas_scfD = row["Fgas[scf/D]"]
    P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

    table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

    expected_Pdrop = df_raw.iloc[2,5:].values * (- 6.89476e3)

    dP_calcs = calc_dP_sections_single_row(table_row, SECTIONS_INFO, expected_Pdrop)

    error_perc = 100.0*(expected_Pdrop - dP_calcs) / expected_Pdrop

    for i in range(len(SECTIONS_INFO)):
        print('Calculated dPf Section {} = {:.2f} (expected = {:.2f}; {:.2f}%)'.format(
            i+1, dP_calcs[i], expected_Pdrop[i], error_perc[i])
        )

def main_run_Pdrop_calcs_on_paper_table():

    df_raw = pd.read_csv("payne-Pdrop.csv")

    n_sections = len(SECTIONS_INFO)

    dP_matrix_output = np.empty((len(df_raw), n_sections))
    for i in range(len(df_raw)):

        row = df_raw.iloc[i,:]
        P_psia = row["P[psia]"]
        T_F = row["T[F]"]
        F_BD = row["F[B/D]"]
        Fgas_scfD = row["Fgas[scf/D]"]
        P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

        table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

        dP_matrix_exp = df_raw.iloc[:,5:].values * (- 6894.76)

        dP_calcs = calc_dP_sections_single_row(table_row, SECTIONS_INFO)

        dP_matrix_output[i, :] = dP_calcs

    error_perc = 100.0*(dP_matrix_exp - dP_matrix_output) / dP_matrix_exp

    x = np.linspace(1, 70, 70)
    y_dP = np.sum(dP_matrix_output, axis=1)
    y_exp = np.sum(dP_matrix_exp, axis=1)
    plt.figure()
    plt.xlabel('linhas')
    plt.ylabel('dP(Pa)')
    plt.plot(x, y_dP, label='dP calc')
    plt.plot(x, y_exp, label='dP exp')
    plt.legend()

    x_exp = np.sum(dP_matrix_exp, axis=1)
    y_dP = np.sum(dP_matrix_output, axis=1)
    y_exp = np.sum(dP_matrix_exp, axis=1)
    plt.figure()
    plt.plot(y_dP, x_exp, 'og', label='dP calc', color='r')
    plt.plot(y_exp, x_exp, 'og', label='dP exp')
    plt.xlabel('dP calc(Pa)')
    plt.ylabel('dP exp(Pa)')
    plt.legend()

    print(dP_matrix_output, error_perc)

def calc_Hl_sections_single_row(table_row, SECTIONS_INFO, expected_Hl=None, print_calcs=False):
    npts = len(SECTIONS_INFO)
    Hl_calcs = np.empty(len(SECTIONS_INFO))
    for i in range(npts):
        row = SECTIONS_INFO[i]
        Hl_tot = 0.0
        for j in range(len(row['params_sections'])):
            parms_dict = row['params_sections'][j]
            length = parms_dict['length']
            elevation = parms_dict['elevation']
            angle = parms_dict['angle']
            my_params_iteration = create_my_parameters_reference(
                table_row
            )
            my_params_iteration.L = length
            my_params_iteration.z = elevation
            my_params_iteration.ang = angle
            calculator_bb = multiphase_equations_3.BeggAndBrillCalculator(my_params_iteration)
            calculator_bb.calculate_dPdL()
            d = calculator_bb.output_as_dict()
            H = d['Hl']
            Hl_tot = Hl_tot + H
        if print_calcs:
            error_perc = 100.0*(Hl_tot - expected_Hl[i]) / expected_Hl[i]
            print('[{}] Calculated Hl Section {} = {:.2f} (expected = {:.2f}; {:.2f}%)'.format(
                'asc' if angle > 0 else 'desc',
                i+1, Hl_tot, expected_Hl[i], error_perc)
            )
        Hl_calcs[i] = Hl_tot
    return Hl_calcs

def main_calc_Hl_with_the_class_single_row():

    print('Hl for Payne row 12105:')

    df_raw = pd.read_csv("payne-Holdups.csv")

    row = df_raw.loc[2]
    P_in = row["P-In[psia]"]
    P_out = row["P-out[psia]"]
    P_psia = (P_in + P_out) / 2
    T_Fin = row["T-In[F]"]
    T_Fout = row["T-Out[F]"]
    T_F = (T_Fin + T_Fout) / 2
    F_BD = row["LiquidRate[B/D]"]
    Fgas_scfD = row["GasRate[scf/D]"]
    Hl_1 = row["sec-1"]
    Hl_2 = row["sec-2"]
    Hl_3 = row["sec-3"]
    Hl_4 = row["sec-4"]
    Hl_5 = row["sec-5b"]
    Hl_6 = row["sec-6"]
    P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

    table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

    expected_Hl = np.array([Hl_1, Hl_2, Hl_3, Hl_4, Hl_5, Hl_6])

    Hl_calcs = calc_Hl_sections_single_row(table_row, SECTIONS_INFO, expected_Hl)

    error_perc = 100.0*(Hl_calcs - expected_Hl) / expected_Hl

    for i in range(len(SECTIONS_INFO)):
        print('Calculated Hl Section {} = {:.2f} (expected = {:.2f}; {:.2f}%)'.format(
            i+1, Hl_calcs[i], expected_Hl[i], error_perc[i])
        )

def main_run_Hl_calcs_on_paper_table():

    df_raw = pd.read_csv("payne-Holdups.csv")

    n_sections = len(SECTIONS_INFO)

    Hl_1 = df_raw.iloc[:,6]
    Hl_2 = df_raw.iloc[:,9]
    Hl_3 = df_raw.iloc[:,7]
    Hl_4 = df_raw.iloc[:,10]
    Hl_5 = df_raw.iloc[:,8]
    Hl_6 = df_raw.iloc[:,11]
    Hl_error = np.array([Hl_1, Hl_2, Hl_3, Hl_4, Hl_5, Hl_6])
    Hl_matrix_exp = Hl_error.T

    Hl_matrix_output = np.empty((len(df_raw), n_sections))
    for i in range(len(df_raw)):

        row = df_raw.iloc[i,:]
        P_in = row["P-In[psia]"]
        P_out = row["P-out[psia]"]
        P_psia = (P_in + P_out) / 2
        T_Fin = row["T-In[F]"]
        T_Fout = row["T-Out[F]"]
        T_F = (T_Fin + T_Fout) / 2
        F_BD = row["LiquidRate[B/D]"]
        Fgas_scfD = row["GasRate[scf/D]"]
        P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

        table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

        Hl_calcs = calc_Hl_sections_single_row(table_row, SECTIONS_INFO)

        Hl_matrix_output[i, :] = Hl_calcs

    error_perc = 100.0*(Hl_matrix_output - Hl_matrix_exp) / Hl_matrix_exp

    plt.figure()
    for i in range(Hl_matrix_exp.shape[1]):
        y_exp = Hl_matrix_exp[:,i]
        y_calc = Hl_matrix_output[:,i]
        plt.subplot(3,2,i+1)
        plt.title('Section: {}'.format(i+1))
        plt.plot(y_calc, y_exp, 'og', label='Holdup calc', color='r')
        plt.plot(y_exp, y_exp, 'og', label='Holdup exp')
        plt.xlabel('Holdup calc')
        plt.ylabel('Holdup exp')
        plt.legend()

    print(Hl_matrix_output, error_perc)

def calc_dHdL_sections_single_row(table_row, SECTIONS_INFO, print_calcs=False):
    npts = len(SECTIONS_INFO)
    dHdL_calcs = np.empty(len(SECTIONS_INFO))
    for i in range(npts):
        row = SECTIONS_INFO[i]
        dHdL_tot = 0.0
        for j in range(len(row['params_sections'])):
            parms_dict = row['params_sections'][j]
            length = parms_dict['length']
            elevation = parms_dict['elevation']
            angle = parms_dict['angle']
            my_params_iteration = create_my_parameters_reference(
                table_row
            )
            my_params_iteration.L = length
            my_params_iteration.z = elevation
            my_params_iteration.ang = angle

            dg = multiphase_equations_3.calc_dg(my_params_iteration)
            U = multiphase_equations_3.calc_U(my_params_iteration)
            Qf = multiphase_equations_3.calc_Qf(U, my_params_iteration)
            Wm = multiphase_equations_3.calc_Wm(dg, my_params_iteration)
            Sp = multiphase_equations_3.calc_Sp(my_params_iteration)
            dHdL = multiphase_equations_3.calc_dHdL(Wm, Sp, Qf, my_params_iteration)
            dHdL_tot = dHdL_tot + dHdL
        if print_calcs:
            print('[{}] Calculated dHdL Section {} = {:.2f}'.format(
                'asc' if angle > 0 else 'desc',
                i+1, dHdL_tot)
            )
        dHdL_calcs[i] = dHdL_tot
    return dHdL_calcs

def main_calc_dHdL_with_the_class_single_row():

    print('dHdL for Payne row 12202:')

    df_raw = pd.read_csv("payne-Pdrop.csv")

    row = df_raw.loc[2]
    P_psia = row["P[psia]"]
    T_F = row["T[F]"]
    F_BD = row["F[B/D]"]
    Fgas_scfD = row["Fgas[scf/D]"]
    P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

    table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

    dHdL_calcs = calc_dHdL_sections_single_row(table_row, SECTIONS_INFO)

    for i in range(len(SECTIONS_INFO)):
        print('Calculated dHdL Section {} = {:.2f}'.format(
            i+1, dHdL_calcs[i])
        )

def main_run_dHdL_calcs_on_paper_table():

    df_raw = pd.read_csv("payne-Pdrop.csv")

    n_sections = len(SECTIONS_INFO)

    dHdL_matrix_output = np.empty((len(df_raw), n_sections))
    for i in range(len(df_raw)):

        row = df_raw.iloc[i,:]
        P_psia = row["P[psia]"]
        T_F = row["T[F]"]
        F_BD = row["F[B/D]"]
        Fgas_scfD = row["Fgas[scf/D]"]
        P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

        table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

        dHdL_calcs = calc_dHdL_sections_single_row(table_row, SECTIONS_INFO)

        dHdL_matrix_output[i, :] = dHdL_calcs

    x = np.linspace(1, 70, 70)
    y_dHdL = np.sum(dHdL_matrix_output, axis=1)
    plt.figure()
    plt.xlabel('linhas')
    plt.ylabel('dHdL(J/kg m)')
    plt.plot(x, y_dHdL, label='dHdL')
    plt.legend()

    print(dHdL_matrix_output)

def calc_H_e_sections_single_row(table_row, SECTIONS_INFO, print_calcs=False):
    npts = len(SECTIONS_INFO)
    H_e_calcs = np.empty(len(SECTIONS_INFO))
    for i in range(npts):
        row = SECTIONS_INFO[i]
        H_e_tot = 0.0
        for j in range(len(row['params_sections'])):
            parms_dict = row['params_sections'][j]
            length = parms_dict['length']
            elevation = parms_dict['elevation']
            angle = parms_dict['angle']
            my_params_iteration = create_my_parameters_reference(
                table_row
            )
            my_params_iteration.L = length
            my_params_iteration.z = elevation
            my_params_iteration.ang = angle

            dg = multiphase_equations_3.calc_dg(my_params_iteration)
            H_m_agua = multiphase_equations_3.calc_H_m_agua(my_params_iteration)
            H_m_gas = multiphase_equations_3.calc_H_m_gas(my_params_iteration)
            Beta = multiphase_equations_3.calc_Beta(dg, my_params_iteration)
            H_e = multiphase_equations_3.calc_H_e(H_m_agua, H_m_gas, Beta, my_params_iteration)
            H_e_tot = H_e_tot + H_e

        if print_calcs:
            print('[{}] Calculated H_e Section {} = {:.2f}'.format(
                'asc' if angle > 0 else 'desc',
                i+1, H_e_tot)
            )
        H_e_calcs[i] = H_e_tot
    return H_e_calcs

def main_calc_H_e_with_the_class_single_row():

    print('H_e for Payne row 12202:')

    df_raw = pd.read_csv("payne-Pdrop.csv")

    row = df_raw.loc[2]
    P_psia = row["P[psia]"]
    T_F = row["T[F]"]
    F_BD = row["F[B/D]"]
    Fgas_scfD = row["Fgas[scf/D]"]
    P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

    table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

    H_e_calcs = calc_H_e_sections_single_row(table_row, SECTIONS_INFO)

    for i in range(len(SECTIONS_INFO)):
        print('Calculated H_e Section {} = {:.2f}'.format(
            i+1, H_e_calcs[i])
        )

def main_run_H_e_calcs_on_paper_table():

    df_raw = pd.read_csv("payne-Pdrop.csv")

    n_sections = len(SECTIONS_INFO)

    H_e_matrix_output = np.empty((len(df_raw), n_sections))
    for i in range(len(df_raw)):

        row = df_raw.iloc[i,:]
        P_psia = row["P[psia]"]
        T_F = row["T[F]"]
        F_BD = row["F[B/D]"]
        Fgas_scfD = row["Fgas[scf/D]"]
        P, T, F, Fgas = funcao_de_conversao_de_unidade(P_psia, T_F, F_BD, Fgas_scfD)

        table_row = {'P': P, 'T': T, 'F': F, 'Fgas': Fgas}

        H_e_calcs = calc_H_e_sections_single_row(table_row, SECTIONS_INFO)

        H_e_matrix_output[i, :] = H_e_calcs

    x = np.linspace(1, 70, 70)
    y_H_e = np.sum(H_e_matrix_output, axis=1)
    plt.figure()
    plt.xlabel('linhas')
    plt.ylabel('H_e(J/kg)')
    plt.plot(x, y_H_e, label='H_e')
    plt.legend()

    print(H_e_matrix_output)

def modelo(x, L):
    H = x[0]
    P = x[1]

    # E.D.O.s:

    my_params = multiphase_equations_3.PhysicalChemicalProperties()

    dg = multiphase_equations_3.calc_dg(my_params)
    U = multiphase_equations_3.calc_U(my_params)
    Sp = multiphase_equations_3.calc_Sp(my_params)
    Qf = multiphase_equations_3.calc_Qf(U, my_params)
    Wm = multiphase_equations_3.calc_Wm(dg, my_params)
    calculator_bb = multiphase_equations_3.BeggAndBrillCalculator(my_params)

    dHdL = multiphase_equations_3.calc_dHdL(Wm, Sp, Qf, my_params)
    dPdL = - calculator_bb.calculate_dPdL()
    return [dHdL, dPdL]

# Condições iniciais:

H0 = 563.68 # J / kg
P0 = multiphase_equations_3.PhysicalChemicalProperties().P0 # Pa

L = np.linspace(0, 15)

y = odeint(modelo,[H0, P0],L)
H = y[:, 0]
P = y[:, 1]

data = np.vstack((L, H.T, P.T))
data = data.T

# Plotando os Gráficos:

plt.figure()
plt.xlabel('Comprimento(m)')
plt.ylabel('H(J/kg)')
plt.plot(L, H)

plt.figure()
plt.xlabel('Comprimento(m)')
plt.ylabel('P(Pa)')
plt.plot(L, P)

if __name__ == '__main__':

    main_calc_dPf_with_the_class_single_row()

    # main_run_Pdrop_calcs_on_paper_table()

    # main_calc_Hl_with_the_class_single_row()

    # main_run_Hl_calcs_on_paper_table()

    # main_calc_dHdL_with_the_class_single_row()

    # main_run_dHdL_calcs_on_paper_table()

    # main_calc_H_e_with_the_class_single_row()

    # main_run_H_e_calcs_on_paper_table()

    # plt.show()

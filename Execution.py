import Multiphase_Flow_Model

# Definindo tipo de fluxo:

def fun_fluxo():
    my_params = Multiphase_Flow_Model.MyParameters()
    Ap = Multiphase_Flow_Model.calc_Ap(my_params)
    vsl = Multiphase_Flow_Model.calc_vsl(Ap, my_params)
    vsg = Multiphase_Flow_Model.calc_vsg(Ap, my_params)
    vm = Multiphase_Flow_Model.calc_vm(vsl, vsg)
    Cl = Multiphase_Flow_Model.calc_Cl(my_params)
    Nfr = Multiphase_Flow_Model.calc_Nfr(vm, my_params)
    L1 = Multiphase_Flow_Model.calc_L1(Cl)
    L2 = Multiphase_Flow_Model.calc_L2(Cl)
    L3 = Multiphase_Flow_Model.calc_L3(Cl)
    L4 = Multiphase_Flow_Model.calc_L4(Cl)
    if (Cl < 0.01 and Nfr < L1) or (Cl >= 0.01 and Nfr < L2):
        print("Segregado")
    elif (0.01 <= Cl < 0.4 and L3 < Nfr <= L1) or (Cl >= 0.4 and L3 < Nfr <= L4):
        print("Intermitente")
    elif (Cl < 0.4 and Nfr >= L1) or (Cl >= 0.4 and Nfr > L4):
        print("Distribuído")
    else:
        print("Transição")

# Desta forma, para os parâmetros de entrada dados, o tipo de fluxo é distribuído.

# Calculando o hold up

def holdup():
    my_params = Multiphase_Flow_Model.MyParameters()
    H = Multiphase_Flow_Model.fun_Hl(my_params)
    print(H)

# Desta forma, calcula-se o hold up como sendo 0,001.

# Calculando o número de Reynolds

def fun_Re():
    my_params = Multiphase_Flow_Model.MyParameters()
    dg = Multiphase_Flow_Model.calc_dg(my_params)
    mil = Multiphase_Flow_Model.calc_mil(my_params)
    mig = Multiphase_Flow_Model.calc_mig(dg, my_params)
    Ap = Multiphase_Flow_Model.calc_Ap(my_params)
    vsl = Multiphase_Flow_Model.calc_vsl(Ap, my_params)
    vsg = Multiphase_Flow_Model.calc_vsg(Ap, my_params)
    vm = Multiphase_Flow_Model.calc_vm(vsl, vsg)
    Cl = Multiphase_Flow_Model.calc_Cl(my_params)
    dn = Multiphase_Flow_Model.calc_dn(dg, Cl, my_params)
    min = Multiphase_Flow_Model.calc_min(mil, mig, Cl)
    Ren = Multiphase_Flow_Model.calc_Re(dn, vm, min, my_params)
    if Ren < 2100:
        print(Ren, 'Regime laminar')
    else:
        print(Ren, 'Regime turbulento')

# Desta forma, calcula-se o número de Reynolds como sendo 26898618,07, sendo, assim, o regime turbulento.

# Calculando a queda de pressão

def calc_dP():
    my_params = Multiphase_Flow_Model.MyParameters()
    dP = Multiphase_Flow_Model.fun_dP(my_params)
    print(dP)

# Desta forma, calcula-se a queda de pressão como sendo 8298878,92 Pa.

if __name__ == '__main__':

    fun_fluxo()

    holdup()

    fun_Re()

    calc_dP()

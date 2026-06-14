import numpy as np
from scipy import constants
from enum import Enum

R = constants.R

class MultiphaseFlowType(Enum):
    SEGREGATED = 'SEGREGATED'
    INTERMITENT = 'INTERMITENT'
    DISTRIBUTED = 'DISTRIBUTED'
    TRANSITION = 'TRANSITION'

class PhysicalChemicalProperties():
    def __init__(self, ql = 0.001, qg = 0.016,
        D = 0.052, e = 0, dl = 999.55, MG = 0.016, ts = 0.06, g = 9.8,
        ang = 0.07, z = 1.12, L = 15.24, T = 296, P0 = 2937167.76,
        z_gas=1.0,
        dg=None, mig=None, mil=None):
        self.ql = ql # m³ / s
        self.qg = qg # m³ / s
        self.D = D # m
        self.e = e # m
        self.dl = dl # Kg / m³
        self.MG = MG # Kg / mol
        self.ts = ts # N / m
        self.g = g # m / s²
        self.ang = ang # rad
        self.z = z # m
        self.L = L # m
        self.T = T # K
        self.P0 = P0 # Pa
        self.z_gas = z_gas # -
        self.dg = dg # kg/m^3
        self.mig = mig # Pa*s
        self.mil = mil # Pa*s

def calc_dg(params):
    # Esta função calcula a densidade do gás(Kg / m³). Eq. 3-88.
    MG = params.MG
    T = params.T
    P0 = params.P0
    z_gas = params.z_gas
    dg = (P0 * MG) / (z_gas * R * T)
    return dg

def calc_mil(params):
    # Esta função calcula a viscosidade do líquido(Pa * s).
    # Equação não utilizada.
    dl = params.dl
    T = params.T
    API = (141.5 / (dl / 1000)) - 131.5
    a = 10 ** (0.43 + (8.33 / API))
    mil = (0.32 + (1.8 * (10 ** 7) / (API ** 4.53))) * ((
        360 / (T + 200)) ** a) * 0.001
    return mil

def calc_mig(dg, params):
    # Esta função calcula a viscosidade do gás(Pa * s). Eq. 3-101.
    MG = params.MG
    T = params.T
    K = ((9.4 + (0.02 * MG * 1000)) * ((9 * T / 5) ** 1.5)) / (
        209 + (19 * MG * 1000) + (9 * T / 5))
    X = 3.5 + (548 / T) + (0.01 * MG * 1000)
    Y = 2.4 - (0.2 * X)
    mig = (1e-7) * K * np.exp(X * (((1e-3) * dg)**Y))
    return mig

def calc_Ap(params):
    # Esta função calcula a área transversal do tubo(m²). Eq. 2-25.
    D = params.D
    Ap = np.pi * (D ** 2) / 4
    return Ap

def calc_vsl(Ap, params):
    # Esta função calcula a velocidade superficial do líquido(m / s).
    # Eq. 2-11.
    ql = params.ql
    vsl = ql / Ap
    return vsl

def calc_vsg(Ap, params):
    # Esta função calcula a velocidade superficial do gás(m / s).
    # Eq. 2-12.
    qg = params.qg
    vsg = qg / Ap
    return vsg

def calc_vm(vsl, vsg):
    # Esta função calcula a velocidade de mistura(m / s). Eq. 2-13.
    vm = vsl + vsg
    return vm

def calc_Cl(params):
    # Esta função calcula a fração volumétrica de entrada. Eq. 2-1.
    ql = params.ql
    qg = params.qg
    Cl = ql / (ql + qg)
    return Cl

def calc_min(mil, mig, Cl):
    # Esta função calcula a viscosidade de não-escorregamento(N x m / s²).
    # Eq. 2-6.
    min = (mil * Cl) + (mig * (1 - Cl))
    return min

def calc_dn(dg, Cl, params):
    # Esta função calcula a densidade de não-escorregamento(kg / m³).
    # Eq. 2-8.
    dl = params.dl
    dn = (dl * Cl) + (dg * (1 - Cl))
    return dn

def calc_L1(Cl):
    # Esta função calcula o adimensional L1. Eq. 2-46.
    L1 = 316 * (Cl ** 0.302)
    return L1

def calc_L2(Cl):
    # Esta função calcula o adimensional L2. Eq. 2-47.
    L2 = 0.0009252 * (Cl**-2.4684)
    return L2

def calc_L3(Cl):
    # Esta função calcula o adimensional L3. Eq. 2-48.
    L3 = 0.1 * (Cl**-1.4516)
    return L3

def calc_L4(Cl):
    # Esta função calcula o adimensional L4. Eq. 2-49.
    L4 = 0.5 * (Cl**-6.738)
    return L4

def calc_Nfr(vm, params):
    # Esta função calcula o número de Froude de mistura.
    # Eq. 2-52.
    D = params.D
    g = params.g
    Nfr = (vm ** 2) / (g * D)
    return Nfr

def calc_Hl0(Cl, L1, L2, L3, L4, Nfr):
    # Esta função calcula a fração volumétrica in-situ para o
    # tubo na posição horizontal. Eq. 2-51.
    if (Cl < 0.01 and Nfr < L1) or (Cl >= 0.01 and Nfr < L2): # Segregado
        Hl0 = 0.98 * (Cl ** 0.4846) * (Nfr ** - 0.0868)
    elif (0.01 <= Cl < 0.4 and L3 < Nfr <= L1) or (
        Cl >= 0.4 and L3 < Nfr <= L4): # Intermitente
        Hl0 = 0.845 * (Cl ** 0.5351) * (Nfr ** - 0.0173)
    else: # Distribuído
        Hl0 = 1.065 * (Cl ** 0.5824) * (Nfr ** - 0.0609)
    return Hl0

def calc_Nlv(vsl, params):
    # Esta função calcula o número de velocidade do líquido.
    # Eq. 2-55.
    dl = params.dl
    g = params.g
    ts = params.ts
    Nvl = vsl * ((dl / (g * ts)) ** 0.25)
    return Nvl

def detect_multiphase_regime(Cl, L1, L2, L3,
L4, Nfr) -> MultiphaseFlowType:
    #Esta função detecta o regime do escoamento
    #
    # refactor: use this equation in calc_Hl0 and calc_C

    if (Cl < 0.01 and Nfr < L1) or (
        Cl >= 0.01 and Nfr < L2): # Segregado
        flow_type = MultiphaseFlowType.SEGREGATED
    elif (0.01 <= Cl < 0.4 and L3 < Nfr <= L1) or (
        Cl >= 0.4 and L3 < Nfr <= L4): # Intermitente
        flow_type = MultiphaseFlowType.INTERMITENT
    elif (Cl < 0.4 and Nfr >= L1) or (
        Cl >= 0.4 and Nfr > L4): # Distribuído
        flow_type = MultiphaseFlowType.DISTRIBUTED
    else:
        flow_type = MultiphaseFlowType.TRANSITION
    return flow_type

def calc_C(Cl, L1, L2, L3, L4, Nfr, Nlv, params):
    # Esta função calcula o adimensional C. Eq. 2-54.
    ang = params.ang
    if ang > 0:
        if (Cl < 0.01 and Nfr < L1) or (
            Cl >= 0.01 and Nfr < L2): # Segregado
            C = (1 - Cl) * np.log(0.011 * (
                Cl ** - 3.768) * (Nfr ** - 1.614) * (Nlv ** 3.539))
        elif (0.01 <= Cl < 0.4 and L3 < Nfr <= L1) or (
            Cl >= 0.4 and L3 < Nfr <= L4): # Intermitente
            C = (1 - Cl) * np.log(2.96 * (
                Cl ** 0.305) * (Nfr ** 0.0978) * (Nlv ** - 0.4473))
        else: # Distribuído
            C = 0
    else:
        C = (1 - Cl) * np.log(4.7 * (Cl ** - 0.3692) * (
            Nfr ** - 0.5056) * (Nlv ** 0.1244))
    return C

def calc_B(C, params):
    # Esta função calcula o fator de inclinação. Eq. 2-53.
    ang = params.ang
    B = 1 + (C * ((np.sin(1.8 * ang)) - (((
        np.sin(1.8 * ang)) ** 3) / 3)))
    return B

def calc_Hl(Cl, L2, L3, Nfr, Nlv, B, Hl0, params):
    # Esta função calcula a fração volumétrica in-situ
    # para o ângulo de inclinação do tubo. Eq. 2-50.
    ang = params.ang
    if Cl>= 0.01 and L2 <= Nfr <= L3: # Transição
        Hlseg = (1 + (((1 - Cl) * np.log(0.011 * (Cl ** - 3.768) * (
            Nfr ** - 1.614) * (Nlv ** 3.539))) * ((
                np.sin(1.8 * ang)) - (((np.sin(
                    1.8 * ang)) ** 3) / 3)))) * 0.98 * (
                        Cl ** 0.4846) * (Nfr ** - 0.0868)
        Hlint = (1 + (((1 - Cl) * np.log(2.96 * (Cl ** 0.305) * (
            Nfr ** 0.0978) * (Nlv ** - 0.4473))) * ((
                np.sin(1.8 * ang)) - (((np.sin(
                    1.8 * ang)) ** 3) / 3)))) * 0.845 * (
                        Cl ** 0.5351) * (Nfr ** - 0.0173)
        A = (L3 - Nfr) / (L3 - L2)
        Hl = (A * Hlseg) + ((1 - A) * Hlint)
    else:
        Hl = B * Hl0
    return Hl

def fun_Hl(params):
    # Esta função calcula a fração volumétrica in-situ para o ângulo
    # de inclinação do tubo, utilizando somente os parâmetros como argumento.

    Ap = calc_Ap(params)
    Cl = calc_Cl(params)
    vsl = calc_vsl(Ap, params)
    vsg = calc_vsg(Ap, params)
    vm = calc_vm(vsl, vsg)
    L1 = calc_L1(Cl)
    L2 = calc_L2(Cl)
    L3 = calc_L3(Cl)
    L4 = calc_L4(Cl)
    Nfr = calc_Nfr(vm, params)
    Hl0 = calc_Hl0(Cl, L1, L2, L3, L4, Nfr)
    Nlv = calc_Nlv(vsl, params)
    C = calc_C(Cl, L1, L2, L3, L4, Nfr, Nlv, params)
    B = calc_B(C, params)
    Hl = calc_Hl(Cl, L2, L3, Nfr, Nlv, B, Hl0, params)
    return Hl

def calc_dtp(dg, Hl, params):
    # Esta função calcula a densidade de mistura(kg / m³).
    # Eq. 2-7.
    dl = params.dl
    dtp = (dl * Hl) + (dg * (1 - Hl))
    return dtp

def calc_dPedL(dtp, params):
    # Esta função calcula o gradiente de pressão por elevação(Pa / m).
    # Eq. 2-70.
    ang = params.ang
    g = params.g
    dPedL = dtp * g * np.sin(ang)
    return dPedL

def calc_y(Cl, Hl):
    # Esta função calcula o adimensional y. Eq. 2-65.
    y = Cl / (Hl ** 2)
    return y

def calc_S(y):
    # Esta função calcula o adimensional S. Eqs. 2-64 e 2-66
    if 1 < y < 1.2:
        S = np.log((2.2 * y) - 1.2)
    else:
        S = (np.log(y)) / (- 0.0523 + (3.182 * np.log(y)) - (
            0.8725 * ((np.log(y)) ** 2)) + (0.01853 * ((np.log(y)) ** 4)))
    return S

def calc_Re(dn, vm, _min, params):
    # Esta função calcula o número de Reynolds. Eq. 2-58.
    D = params.D
    Re = dn * vm * D / _min
    return Re

def calc_fn(Re, params):
    # Esta função calcula o fator de atrito de não-escorregamento.
    # Eqs. 2-60 e 2-61.
    D = params.D
    e = params.e
    er = e / D
    if Re < 2100: # Laminar
        fn = 64 / Re
    else: # Turbulento
        fn = ((1) / (- 2 * np.log10((er / 3.7065) - ((
            5.0452 / Re) * np.log10(((er ** 1.1098) / 2.8257) + (
                5.8506 / (Re ** 0.8981))))))) ** 2
    return fn

def calc_ftp(fn, S):
    # Esta função calcula o fator de atrito de Fanning. Eq. 2-63.
    ftp = fn * np.exp(S)
    return ftp

def calc_dPadL(ftp, dn, vm, params):
    # Esta função calcula o gradiente de pressão por atrito(Pa / m).
    # Eq. 2-69.
    D = params.D
    dPadL = ftp * dn * (vm ** 2) / (2 * D)
    return dPadL

def calc_dPdL(dPadL, dPedL, dtp, vm, vsg, params):
    # Esta função calcula o gradiente de pressão total(Pa/m). Eq. 2-80.
    P0 = params.P0
    dPdL = (dPadL + dPedL) / (1 - (dtp * vm * vsg / P0))
    return dPdL

def calculate_dPdL(params):
    # Esta função calcula o gradiente de pressão utilizando somente
    # os parâmetros como argumento(Pa / m).
    dg = params.dg or calc_dg(params)
    mig = params.mig or calc_mig(dg, params)
    mil = params.mil or calc_mil(params)
    Ap = calc_Ap(params)
    Cl = calc_Cl(params)
    vsl = calc_vsl(Ap, params)
    vsg = calc_vsg(Ap, params)
    vm = calc_vm(vsl, vsg)
    min = calc_min(mil, mig, Cl)
    dn = calc_dn(dg, Cl, params)
    L1 = calc_L1(Cl)
    L2 = calc_L2(Cl)
    L3 = calc_L3(Cl)
    L4 = calc_L4(Cl)
    Nfr = calc_Nfr(vm, params)
    Hl0 = calc_Hl0(Cl, L1, L2, L3, L4, Nfr)
    Nlv = calc_Nlv(vsl, params)
    C = calc_C(Cl, L1, L2, L3, L4, Nfr, Nlv, params)
    B = calc_B(C, params)
    Hl = calc_Hl(Cl, L2, L3, Nfr, Nlv, B, Hl0, params)
    dtp = calc_dtp(dg, Hl, params)
    dPedL = calc_dPedL(dtp, params)
    y = calc_y(Cl, Hl)
    S = calc_S(y)
    Re = calc_Re(dn, vm, min, params)
    fn = calc_fn(Re, params)
    ftp = calc_ftp(fn, S)
    dPadL = calc_dPadL(ftp, dn, vm, params)
    dPdL = calc_dPdL(dPadL, dPedL, dtp, vm, vsg, params)
    return dPdL



class BeggAndBrillCalculator():

    def __init__(self, params) -> None:
        self.params = params
        pass

    def calculate_dPdL(self) -> float:
        params = self.params
        self.dg = params.dg or calc_dg(params)
        self.mig = params.mig or calc_mig(self.dg, params)
        self.mil = params.mil or calc_mil(params)
        self.Ap = calc_Ap(params)
        self.Cl = calc_Cl(params)
        self.vsl = calc_vsl(self.Ap, params)
        self.vsg = calc_vsg(self.Ap, params)
        self.vm = calc_vm(self.vsl, self.vsg)
        self.min = calc_min(self.mil, self.mig, self.Cl)
        self.dn = calc_dn(self.dg, self.Cl, params)
        self.L1 = calc_L1(self.Cl)
        self.L2 = calc_L2(self.Cl)
        self.L3 = calc_L3(self.Cl)
        self.L4 = calc_L4(self.Cl)
        self.Nfr = calc_Nfr(self.vm, params)
        self.flow_type = detect_multiphase_regime(
            self.Cl, self.L1, self.L2, self.L3, self.L4, self.Nfr)
        self.Hl0 = calc_Hl0(self.Cl, self.L1,
        self.L2, self.L3, self.L4, self.Nfr)
        self.Nlv = calc_Nlv(self.vsl, params)
        self.C = calc_C(self.Cl, self.L1, self.L2, self.L3, self.L4,
        self.Nfr, self.Nlv, params)
        self.B = calc_B(self.C, params)
        self.Hl = calc_Hl(self.Cl, self.L2, self.L3, self.Nfr,
        self.Nlv, self.B, self.Hl0, params)
        self.dtp = calc_dtp(self.dg, self.Hl, params)
        self.dPedL = calc_dPedL(self.dtp, params)
        self.y = calc_y(self.Cl, self.Hl)
        self.S = calc_S(self.y)
        self.Re = calc_Re(self.dn, self.vm, self.min, params)
        self.fn = calc_fn(self.Re, params)
        self.ftp = calc_ftp(self.fn, self.S)
        self.dPadL = calc_dPadL(self.ftp, self.dn, self.vm, params)
        self.dPdL = calc_dPdL(self.dPadL, self.dPedL, self.dtp,
        self.vm, self.vsg, params)
        return self.dPdL

    def output_as_dict(self) -> dict:
        d = {
            'dg': self.dg,
            'mig': self.mig,
            'mil': self.mil,
            'Ap': self.Ap,
            'Cl': self.Cl,
            'vsl': self.vsl,
            'vsg': self.vsg,
            'vm': self.vm,
            'min': self.min,
            'dn': self.dn,
            'L1': self.L1,
            'L2': self.L2,
            'L3': self.L3,
            'L4': self.L4,
            'Nfr': self.Nfr,
            'flow_type': self.flow_type,
            'Hl0': self.Hl0,
            'Nlv': self.Nlv,
            'C': self.C,
            'B': self.B,
            'Hl': self.Hl,
            'dtp': self.dtp,
            'dPedL': self.dPedL,
            'y': self.y,
            'S': self.S,
            'Re': self.Re,
            'fn': self.fn,
            'ftp': self.ftp,
            'dPadL': self.dPadL,
            'dPdL': self.dPdL,
        }
        return d

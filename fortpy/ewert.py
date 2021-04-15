# %%
from dataclasses import dataclass
from fewert import ewert as fewert

t_lem_constant = 0.15
t_lse_constant = 0.33

t_l = 800
t_lem = t_l * t_lem_constant
t_lma = t_l - t_lem
t_lse = t_lma * t_lse_constant
t_lep = t_l - (t_lem + t_lse)  # check this


@dataclass
class ModelOptions:
    """Ewert model options.

    opt_full_night_recovery: bool
        If True leaf recovers every none daylight hour, else only at hr==0
    use_O3_damage: bool
        If true pass O3_acc and O3 into model which enables fO3_d and f_LS
    f_VPD_method: str
        If "photosynthesis" then f_VPD is calculated internally else should be provided as input
    """
    opt_full_night_recovery: bool = False
    use_O3_damage: bool = True
    f_VPD_method: str = "photosynthesis"


@dataclass
class CO2_loop_State:
    """Variables that change over the CO2 convergence loop.

    Parameters
    ----------
    c_i: float
        CO2 concentration inside stomata [umol CO2]
    c_i_diff: float
        difference in c_i between iterations [ppm]
    g_sto: float
        stomatal conductance within the loop [umol/ m^2/s gsto]
    f_LS: float
        factor effect of leaf senescence on A_c [Dimensionless][0-1]
    f_LA: float
        factor effect of ... [Dimensionless][0-1]
    A_n: float
        eq 1 - CO2 Assimilation Rate  [umol m-2 s-1 CO2]
    A_c: float
        eq 8 - Rubisco activity limited rate of photosynthesis [umol m-2 s-1 CO2]
    A_p: float
        eq ? - Triose phosphate utilisation limited assimilation rate [umol m-2 s-1 CO2]
    A_j: float
        eq 3 - RuBP regeneration (electron transport) limited assimilation rate (A_q in paper)
         [umol m-2 s-1 CO2]
    A_n_limit_factor: str
        The factor that has limited CO2 assimilation (A_c/A_j/A_p)
    fO3_d: float
        Hourly accumulated ozone impace factor [dimensionless][0-1] ___
    fO3_h: float
        Hourly ozone impace factor [dimensionless][0-1] ___
    fO3_l: float
        Ozone exposure [umol/m^2 gsto]
    iterations: float
        Number of iterations in convergence loop
    t_lep_ozone: float
        ozone adjusted t_lep
    t_lma_ozone: float
        ozone adjusted t_lma
    t_lse_ozone: float
        ozone adjusted t_lse
    t_l_ozone: float
        ozone adjusted t_l
    f_VPD: float
        Humidity Function (Leuning 1995)
    """

    c_i: float
    c_i_diff: float
    g_sto: float
    f_LS: float = 0.0
    f_LA: float = 0.0
    A_n: float = 0.0
    A_c: float = 0.0
    A_p: float = 0.0
    A_j: float = 0.0
    A_n_limit_factor: str = None
    fO3_d: float = 1.0
    fO3_h: float = 1.0
    fO3_l: float = 0.0
    iterations: int = 0
    t_lep_ozone: float = None
    t_lma_ozone: float = None
    t_lse_ozone: float = None
    t_l_ozone: float = None
    f_VPD: float = None


@dataclass
class CO2_Constant_Loop_Inputs():
    """Inputs to the CO2_convergence loop that remain constant throughout loop.

    Parameters
    ------
    D_0: float
        "The VPD at which g_sto is reduced by a factor of 2" [Pa] (Leuning et al. 1998)
    c_a: float
        CO2 concentration [ppm]
    e_a: float
        Ambient vapour pressure [Pa]
    g_bl: float
        Boundary layer conductance to H2O vapour [umol m-2 PLA s-1 H2O?]
    g_sto_0: float
        Closed stomata conductance [umol/m^2/s CHECK GAS]
    m: float
        Species-specific sensitivity to An [dimensionless]
    O3up: float
        Ozone uptake (fst) [nmol O3 PLA m-2 s-1 O3]
    O3up_acc: float
        Accumulated Ozone uptake [nmol O3 PLA m-2 s-1 O3]
    fO3_d_prev: float
        Cumulative ozone effect from previous hour [dimensionless][0-1]
    td_dd: float
        difference between current td and td at season_Astart [Thermal Time]
    gamma_1: float
        short term damage coefficient [dimensionless]
    gamma_2: float
        short term damage coefficient [nmol m-2 O3?]
    gamma_3: float
        long term damage coefficient [umol m-2 O3?]
    is_daylight: float
        True when PAR > 50 W m^2 [bool]
    t_lse_constant: float
            t_lse as fraction of t_l [Thermal Time]
    t_l_estimate: float
        Full estimated life span of leaf in thermal time [Thermal Time]
    t_lem: float
        time from seed to end of emerging leaf/start of mature leaf [Thermal Time]
    t_lep: float
        Time during which leaf is expanding [Thermal Time]
    t_lse: float
        Time that the leaf is senescing [Thermal Time]
    t_lma: float
        Full time of mature leaf (t_lep + t_lse) [Thermal Time]
    Gamma: float
        CO2 compensation point [umol/mol CO2]
    Gamma_star: float
        # CO2 comp. point without day resp.  [umol/mol CO2]
    V_cmax: float
        Max catalytic rate of Rubisco [umol/(m^2*s) CO2]
    K_C: float
        Michaelis constant CO2 [umol/mol CHECK GAS]
    K_O: float
        Michaelis constant O2 [mmol/mol CHECK GAS]
    J: float
        Rate of electron transport [umol/(m^2*s) CHECK GAS]
    R_d: float
        day respiration rate [umol/(m^2*s) CHECK GAS]
    e_sat_i: float
        internal saturation vapour pressure[Pa]
    hr: int
        Hour of day [0-23]
    f_SW: float
        Soil water influence on photosynthesis [0-1]
    f_VPD: float
        VPD effect on gsto [fraction] (Optional if pre-calculated)
    """

    c_a: float
    e_a: float
    g_bl: float
    g_sto_0: float
    m: float
    D_0: float
    O3up: float
    O3up_acc: float
    fO3_d_prev: float
    td_dd: float
    gamma_1: float
    gamma_2: float
    gamma_3: float
    is_daylight: bool
    t_lse_constant: float
    t_l_estimate: float
    t_lem: float
    t_lep: float
    t_lse: float
    t_lma: float
    Gamma: float
    Gamma_star: float
    V_cmax: float
    K_C: float
    K_O: float
    J: float
    R_d: float
    e_sat_i: float
    hr: int
    f_SW: float
    f_VPD: float = None


constant_inputs = CO2_Constant_Loop_Inputs(
    c_a=391.0,
    e_a=1000.0,
    g_bl=1469999.0,
    g_sto_0=20000,
    m=8.12,
    D_0=2.27 * 1e3,
    O3up_acc=300,
    O3up=21.0,
    fO3_d_prev=0.89,
    td_dd=24.1,
    gamma_1=0.06,
    gamma_2=0.0045,
    gamma_3=0.5,
    is_daylight=True,
    t_lse_constant=t_lse_constant,
    t_l_estimate=t_l,
    t_lem=t_lem,
    t_lep=t_lep,
    t_lse=t_lse,
    t_lma=t_lma,
    Gamma=34.277,
    Gamma_star=32.95,
    V_cmax=119.0,
    K_C=234.42,
    K_O=216.75,
    J=300.36,
    R_d=0.32,
    e_sat_i=2339.05,
    hr=12,
    f_SW=1,
    f_VPD=1.0,
)
loop_state = CO2_loop_State(
    c_i=0.0,
    c_i_diff=0,
    g_sto=20000,
    A_n=0,
    fO3_d=1.0,
    fO3_h=1.0,
)
model_options = ModelOptions(
    use_O3_damage=True,
    opt_full_night_recovery=True,
    f_VPD_method="photosynthesis",
)

out = fewert.co2_concentration_in_stomata_iteration(
    constant_inputs.c_a,
    constant_inputs.e_a,
    constant_inputs.g_bl,
    constant_inputs.g_sto_0,
    constant_inputs.m,
    constant_inputs.D_0,
    constant_inputs.O3up,
    constant_inputs.O3up_acc,
    constant_inputs.fO3_d_prev,
    constant_inputs.td_dd,
    constant_inputs.gamma_1,
    constant_inputs.gamma_2,
    constant_inputs.gamma_3,
    constant_inputs.is_daylight,
    constant_inputs.t_lse_constant,
    constant_inputs.t_l_estimate,
    constant_inputs.t_lem,
    constant_inputs.t_lep,
    constant_inputs.t_lse,
    constant_inputs.t_lma,
    constant_inputs.Gamma,
    constant_inputs.Gamma_star,
    constant_inputs.V_cmax,
    constant_inputs.K_C,
    constant_inputs.K_O,
    constant_inputs.J,
    constant_inputs.R_d,
    constant_inputs.e_sat_i,
    constant_inputs.hr,
    constant_inputs.f_SW,
    constant_inputs.f_VPD,
    loop_state.c_i,
    loop_state.g_sto,
    model_options.opt_full_night_recovery
)
print(out)

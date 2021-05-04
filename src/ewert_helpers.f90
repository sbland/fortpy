module ewert_helpers
    use ewert_types
    implicit none

    public :: calc_ozone_damage_factors
    public :: calc_ozone_impact_on_lifespan
    public :: calc_senescence_factor
    public :: calc_CO2_assimilation_rate
    public:: calc_humidity_defecit_fVPD
    public:: calc_stomatal_conductance
    public::calc_CO2_supply

    contains

    Pure Real Function calc_fO3_h(O3up, gamma_1, gamma_2) result(fO3_h)
        REAL, intent(in) :: O3up
        REAL, intent(in) :: gamma_1
        REAL, intent(in) :: gamma_2

        REAL::lower_bound
        REAL::upper_bound

        lower_bound = gamma_1 / gamma_2
        upper_bound = (1 + gamma_1) / gamma_2

        if (O3up <= lower_bound) then
            fO3_h = 1
        ELSE if( O3up >= upper_bound)then
            fO3_h = 0
        ELSE
            fO3_h = 1 + gamma_1 - gamma_2 * O3up
        endif
    end function


    Pure Function calc_f_LA(t_lem, t_lma, td_dd) result(f_LA)
        REAL, intent(in) :: t_lem
        REAL, intent(in) :: t_lma
        REAL, intent(in) :: td_dd

        REAL::lower_bound
        REAL::upper_bound
        REAL::f_LA

        lower_bound = t_lem
        upper_bound = t_lem + t_lma

        if( td_dd <= lower_bound) then
            f_LA = 1
        ELSE if( td_dd >= upper_bound) then
            f_LA = 0
        ELSE
            f_LA = 1 - (td_dd - t_lem) / (t_lma)
        endif

    end function

    PURE Type(Damage_Factors) Function calc_ozone_damage_factors(&
        gamma_1, &
        gamma_2, &
        gamma_3, &
        O3up, &
        O3up_acc, &
        fO3_d_prev, &
        td_dd, &
        t_lem, &
        t_lma, &
        is_daylight, &
        hr, &
        opt_full_night_recovery &
    )
        REAL, intent(in):: gamma_1
        REAL, intent(in):: gamma_2
        REAL, intent(in):: gamma_3
        REAL, intent(in):: O3up
        REAL, intent(in):: O3up_acc
        REAL, intent(in):: fO3_d_prev
        REAL, intent(in):: td_dd
        REAL, intent(in):: t_lem
        REAL, intent(in):: t_lma
        LOGICAL, intent(in):: is_daylight
        INTEGER, intent(in):: hr
        LOGICAL, intent(in):: opt_full_night_recovery

        REAL:: fO3_h
        REAL:: fO3_d
        REAL:: fO3_l
        REAL:: f_LA
        REAL:: rO3

        REAL:: fO3_d_base
        REAL:: fO3_d_night

        fO3_h = calc_fO3_h(O3up, gamma_1, gamma_2)
        f_LA = calc_f_LA(t_lem, t_lma, td_dd)
        rO3 = fO3_d_prev + (1 - fO3_d_prev) * f_LA  ! eq 13

        fO3_d_base = fO3_d_prev * fO3_h  ! eq 11 fO3_d degrades during the day
        fO3_d_night = rO3 * fO3_h  ! eq 12  fO3_d recovers during the night
        IF (opt_full_night_recovery) THEN
            IF (is_daylight) THEN
                fO3_d = fO3_d_base
            ELSE
                fO3_d = fO3_d_night
            ENDIF
        ELSE
            IF (hr == 0) THEN
                fO3_d = fO3_d_night
            ELSE
                fO3_d = fO3_d_base
            ENDIF
        ENDIF
        fO3_l = 1 - (gamma_3 * (O3up_acc / 1000))  ! eq 17 ! note conversion to umol

        calc_ozone_damage_factors = Damage_Factors(fO3_h,fO3_d,fO3_l,f_LA,rO3)

    end function

    Pure Type(Leaf_Life_Span_Values) function calc_ozone_impact_on_lifespan( &
        t_lse_constant, &
        t_lep, &
        t_lse, &
        t_lem, &
        fO3_l &
    ) result(lifespan_with_ozone)

        REAL, intent(in) :: t_lse_constant
        REAL, intent(in) :: t_lep
        REAL, intent(in) :: t_lse
        REAL, intent(in) :: t_lem
        REAL, intent(in) :: fO3_l

        REAL t_lma_O3
        REAL t_lse_O3
        REAL t_lep_O3
        REAL t_l_O3

        t_lma_O3 = (t_lep + t_lse) * fO3_l ! eq 16! reduces estimated leaf age by accumulated fst
        t_lse_O3 = t_lse_constant * t_lma_O3 ! make senescing period 0.33 * life span of mature leaf
        ! non senescing period assumed to be remaining time
        t_lep_O3 = t_lma_O3 - t_lse_O3
        t_l_O3 = t_lem + t_lma_O3

        lifespan_with_ozone = Leaf_Life_Span_Values( &
            t_lma=t_lma_O3, &
            t_lse=t_lse_O3, &
            t_lep=t_lep_O3, &
            t_l=t_l_O3 &
        )
    end function

    Pure REAL function calc_senescence_factor(&
        td_dd, &
        t_l_O3, &
        t_lem, &
        t_lep_O3, &
        t_lse_O3 &
        ) result(f_LS)

        REAL, intent(in) :: td_dd
        REAL, intent(in) :: t_l_O3
        REAL, intent(in) :: t_lem
        REAL, intent(in) :: t_lep_O3
        REAL, intent(in) :: t_lse_O3

        REAL :: s_signal

        s_signal = t_lem + t_lep_O3  ! new senescense signal

        IF (td_dd <= s_signal) THEN
            f_LS = 1
        ELSE IF( td_dd >= t_l_O3) THEN
            f_LS = 0
        ELSE
            ! NOTE: Below function
            f_LS = 1 - ((td_dd - t_lem - t_lep_O3) / t_lse_O3)
            ! f_LS = 1 - ((td_dd - t_lem - t_lep_O3) / (t_lma / fO3_l - t_lep_O3))
        ENDIF

    end function

    PURE TYPE(CO2_assimilation_rate_factors) function calc_CO2_assimilation_rate(&
        c_i_in, &
        V_cmax, &
        Gamma_star, &
        K_C, &
        K_O, &
        fO3_d, &
        f_LS, &
        J, &
        R_d &
    ) result(out)
    REAL, intent(in) :: c_i_in
    REAL, intent(in) :: V_cmax
    REAL, intent(in) :: Gamma_star
    REAL, intent(in) :: K_C
    REAL, intent(in) :: K_O
    REAL, intent(in) :: fO3_d
    REAL, intent(in) :: f_LS
    REAL, intent(in) :: J
    REAL, intent(in) :: R_d

    REAL::A_c
    REAL::A_j
    REAL::A_p
    REAL::A_n

    real, parameter :: A_j_a = 4.0           !electron requirement for NADPH formation
    real, parameter :: A_j_b = 8.0           !electron requirement for ATP formation
    real, parameter :: O_i = 210.0           !O2 concentration                   [mmol/mol]


    A_c = V_cmax * ((c_i_in - Gamma_star)  /& ! noqa: W504
                    (c_i_in + (K_C * (1 + (O_i / K_O))))) * fO3_d * f_LS
    A_j = J * ((c_i_in - Gamma_star) / ((A_j_a * c_i_in) + (A_j_b * Gamma_star)))

    A_p = 0.5 * V_cmax

    A_n = min(A_c, A_j, A_p) - R_d

    ! A_n_limit_factor = sorted(
    !     zip(['A_c', 'A_j', 'A_p'], [A_c, A_j, A_p]), key=lambda tup: tup[1])[0][0]

    out = CO2_assimilation_rate_factors(&
        A_c=A_c, &
        A_j=A_j, &
        A_p=A_p, &
        A_n=A_n, &
        A_n_limit_factor=0 &
    )

    end function

    PURE REAL function calc_humidity_defecit_fVPD(&
     g_sto_in, &
     e_a, &
     g_bl, &
     e_sat_i, &
     D_0 &
    ) result(f_VPD)
        REAL, intent(in):: g_sto_in
        REAL, intent(in):: e_a
        REAL, intent(in):: g_bl
        REAL, intent(in):: e_sat_i
        REAL, intent(in):: D_0

        REAL::g_sto_in_mol
        REAL::g_bl_mol
        REAL::h_s
        REAL::d_s
        REAL::e_sat_i_kPa
        REAL::e_a_kPa

        ! Unit conversions
        ! Equation 5 is in mol
        ! Convert from umol to mol
        g_sto_in_mol = g_sto_in * 1e-6
        g_bl_mol = g_bl * 1e-6

        e_sat_i_kPa = e_sat_i * 1e-3
        e_a_kPa = e_a * 1e-3
        ! Surface humidity (Unitless)
        h_s = (g_sto_in_mol * e_sat_i_kPa + g_bl_mol * e_a_kPa) / (e_sat_i_kPa * (g_sto_in_mol + g_bl_mol))
        ! Convert relative humidity to VPD
        d_s = e_sat_i_kPa - (e_sat_i_kPa * h_s)
        f_VPD = 1 / (1 + (d_s / D_0))
    end function

    PURE REAL function calc_stomatal_conductance(&
        g_sto_0, &
        m, &
        Gamma, &
        g_bl, &
        c_a, &
        A_n, &
        f_SW, &
        f_VPD &
    ) result(g_sto)
    REAL, intent(in) :: g_sto_0
    REAL, intent(in) :: m
    REAL, intent(in) :: Gamma
    REAL, intent(in) :: g_bl
    REAL, intent(in) :: c_a
    REAL, intent(in) :: A_n
    REAL, intent(in) :: f_SW
    REAL, intent(in) :: f_VPD

    REAL:: g_sto_0_mol
    REAL:: g_bl_mol
    REAL:: c_s
    REAL:: g_eq_top
    REAL:: g_eq_bottom
    REAL:: g_sto_out_mol

    ! Unit conversions
    ! Equation 5 is in mol
    ! Convert from umol to mol
    g_sto_0_mol = g_sto_0 * 1e-6
    g_bl_mol = g_bl * 1e-6
    ! NOTE: micro mol/(m^2*s) values are not converted

    ! Surface CO2
    ! g_bl converted from H2O to CO2
    c_s = c_a - (A_n * (1.37 / g_bl_mol))

    ! Stomatal conductance

    ! FROM OLD CODE ====
    ! Equation 5 from Ewert paper (scaled by 1e6)
    ! g_sto = g_sto_0 + m * (A_n / ((1 + (h_s_VPD / D_0)) * (c_s - Gamma))) * 1e6
    ! =================

    ! Equation 5 from Ewert paper and Leuning 1995
    ! Equation split up below

    ! TODO: Can replace (1 + (h_s_VPD / D_0) with f_VPD?

    g_eq_top = m * A_n * f_SW * f_VPD  ! micro mol/(m^2*s)
    g_eq_bottom = (c_s - Gamma)  ! f_VPD = 1 + (D_s/D_0)
    g_sto_out_mol = g_sto_0_mol + (g_eq_top / g_eq_bottom)
    ! Convert from mol to umol
    g_sto = g_sto_out_mol * 1e6

    end function

    pure REAL function calc_CO2_supply(&
        A_n, &
        c_a, &
        g_sto, &
        g_bl &
        ) result(c_i_sup)
    REAL, intent(in):: A_n
    REAL, intent(in):: c_a
    REAL, intent(in):: g_sto
    REAL, intent(in):: g_bl

    ! NOTE: umol to mol conversions taken into account for g_sto and g_bl

    ! gsto does not need converting here as already in CO2 umol
    ! g_bl is converted from H2O to CO2 using Dratio
    ! TODO: Check ratio used for g_bl conversion
    c_i_sup = c_a - ((A_n * (1 / g_sto + 1.37 / g_bl)) * 1e6)

    end function

end module
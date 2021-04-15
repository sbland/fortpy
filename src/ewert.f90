module ewert
    use ewert_types
    use ewert_helpers
    implicit none

    contains


    Pure Function co2_concentration_in_stomata_iteration(&
        const_c_a, &
        const_e_a, &
        const_g_bl, &
        const_g_sto_0, &
        const_m, &
        const_D_0, &
        const_O3up, &
        const_O3up_acc, &
        const_fO3_d_prev, &
        const_td_dd, &
        const_gamma_1, &
        const_gamma_2, &
        const_gamma_3, &
        const_is_daylight, &
        const_t_lse_constant, &
        const_t_l_estimate, &
        const_t_lem, &
        const_t_lep, &
        const_t_lse, &
        const_t_lma, &
        const_Gamma, &
        const_Gamma_star, &
        const_V_cmax, &
        const_K_C, &
        const_K_O, &
        const_J, &
        const_R_d, &
        const_e_sat_i, &
        const_hr, &
        const_f_SW, &
        const_f_VPD, &
        c_i_in, &
        g_sto_in, &
        opt_full_night_recovery) result(out)

        REAL,  intent(in) :: const_c_a
        REAL,  intent(in) :: const_e_a
        REAL,  intent(in) :: const_g_bl
        REAL,  intent(in) :: const_g_sto_0
        REAL,  intent(in) :: const_m
        REAL,  intent(in) :: const_D_0
        REAL,  intent(in) :: const_O3up
        REAL,  intent(in) :: const_O3up_acc
        REAL,  intent(in) :: const_fO3_d_prev
        REAL,  intent(in) :: const_td_dd
        REAL,  intent(in) :: const_gamma_1
        REAL,  intent(in) :: const_gamma_2
        REAL,  intent(in) :: const_gamma_3
    LOGICAL,  intent(in)::   const_is_daylight
        REAL,  intent(in) :: const_t_lse_constant
        REAL,  intent(in) :: const_t_l_estimate
        REAL,  intent(in) :: const_t_lem
        REAL,  intent(in) :: const_t_lep
        REAL,  intent(in) :: const_t_lse
        REAL,  intent(in) :: const_t_lma
        REAL,  intent(in) :: const_Gamma
        REAL,  intent(in) :: const_Gamma_star
        REAL,  intent(in) :: const_V_cmax
        REAL,  intent(in) :: const_K_C
        REAL,  intent(in) :: const_K_O
        REAL,  intent(in) :: const_J
        REAL,  intent(in) :: const_R_d
        REAL,  intent(in) :: const_e_sat_i
    INTEGER,  intent(in)::   const_hr
        REAL,  intent(in) :: const_f_SW
        REAL,  intent(in) :: const_f_VPD
        REAL,  intent(in) :: c_i_in
        REAL,  intent(in) :: g_sto_in
        LOGICAL, intent(in) :: opt_full_night_recovery

        TYPE (Damage_Factors) :: ozone_damage_factors
        ! TYPE (Leaf_Life_Span_Values) :: lifespan_with_ozone
        REAL, dimension(3) :: out

        ! 2. Run calculations

        ozone_damage_factors = calc_ozone_damage_factors( &
            gamma_1=const_gamma_1, &
            gamma_2=const_gamma_2, &
            gamma_3=const_gamma_3, &
            O3up=const_O3up, &
            O3up_acc=const_O3up_acc, &
            fO3_d_prev=const_fO3_d_prev, &
            td_dd=const_td_dd, &
            t_lem=const_t_lem, &
            t_lma=const_t_lma, &
            is_daylight=const_is_daylight, &
            hr=const_hr, &
            opt_full_night_recovery=opt_full_night_recovery &
        )


        ! lifespan_with_ozone = calc_ozone_impact_on_lifespan( &
        !     t_lse_constant=const_t_lse_constant, &
        !     t_lep=const_t_lep, &
        !     t_lse=const_t_lse, &
        !     t_lem=const_t_lem, &
        !     fO3_l=ozone_damage_factors%fO3_l &
        ! )



        ! f_LS = calc_senescence_factor(
        !     td_dd=const_td_dd,
        !     ! t_l_estimate=const_t_l_estimate,
        !     t_l_O3=lifespan_with_ozone.t_l_O3,
        !     ! fO3_l=ozone_damage_factors.fO3_l,
        !     t_lem=const_t_lem,
        !     t_lep_O3=lifespan_with_ozone.t_lep_O3,
        !     ! t_lma=lifespan_with_ozone.t_lma_O3,
        !     t_lse_O3=lifespan_with_ozone.t_lse_O3,
        ! )

        ! co2_assimilation_rate_values = calc_CO2_assimilation_rate(
        !     c_i_in=c_i_in,
        !     V_cmax=const_V_cmax,
        !     Gamma_star=const_Gamma_star,
        !     K_C=const_K_C,
        !     K_O=const_K_O,
        !     fO3_d=ozone_damage_factors.fO3_d,
        !     f_LS=f_LS,
        !     J=const_J,
        !     R_d=const_R_d,
        ! )

        ! f_VPD = calc_humidity_defecit_fVPD(
        !     g_sto_in=g_sto_in,
        !     e_a=const_e_a,
        !     g_bl=const_g_bl,
        !     e_sat_i=const_e_sat_i,
        !     D_0=const_D_0,
        ! ) if model_options.f_VPD_method == "photosythesis" else const_f_VPD

        ! g_sto = calc_stomatal_conductance(
        !     g_sto_0=const_g_sto_0,
        !     m=const_m,
        !     Gamma=const_Gamma,
        !     g_bl=const_g_bl,
        !     c_a=const_c_a,
        !     A_n=co2_assimilation_rate_values.A_n,
        !     f_SW=const_f_SW,
        !     f_VPD=f_VPD,
        ! )

        ! co2_supply = calc_CO2_supply(
        !     A_n=co2_assimilation_rate_values.A_n,
        !     c_a=const_c_a,
        !     g_sto=g_sto,
        !     g_bl=const_g_bl,
        ! )

        ! c_i = c_i_in - (c_i_in - co2_supply) / 2


        out=0.0
        out(1) = ozone_damage_factors%fO3_h
        ! out(2) = lifespan_with_ozone%t_l
    End Function

end module ewert

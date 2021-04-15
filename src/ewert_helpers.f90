module ewert_helpers
    use ewert_types
    implicit none

    public :: calc_ozone_damage_factors

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
        else if( O3up >= upper_bound)then
            fO3_h = 0
        else
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
        else if( td_dd >= upper_bound) then
            f_LA = 0
        else
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

    ! Pure REAL function calc_senescence_factor() result(f_LS)

end module
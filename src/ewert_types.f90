module ewert_types
    implicit none


    TYPE :: CO2_Constant_Loop_Inputs
        REAL:: c_a
        REAL:: e_a
        REAL:: g_bl
        REAL:: g_sto_0
        REAL:: m
        REAL:: D_0
        REAL:: O3up
        REAL:: O3up_acc
        REAL:: fO3_d_prev
        REAL:: td_dd
        REAL:: gamma_1
        REAL:: gamma_2
        REAL:: gamma_3
        REAL:: is_daylight
        REAL:: t_lse_constant
        REAL:: t_l_estimate
        REAL:: t_lem
        REAL:: t_lep
        REAL:: t_lse
        REAL:: t_lma
        REAL:: Gamma
        REAL:: Gamma_star
        REAL:: V_cmax
        REAL:: K_C
        REAL:: K_O
        REAL:: J
        REAL:: R_d
        REAL:: e_sat_i
        REAL:: hr
        REAL:: f_SW
    end type

    TYPE:: Damage_Factors
        REAL:: fO3_h
        REAL:: fO3_d
        REAL:: fO3_l
        REAL:: f_LA
        REAL:: rO3
    end type

    TYPE:: Leaf_Life_Span_Values
    ! """Values associated with leaf lifespan."""

        REAL:: t_lma
        REAL:: t_lse
        REAL:: t_lep
        REAL:: t_l
    end type

    TYPE::CO2_assimilation_rate_factors
    ! """Variables associated with CO2 assimilation rate."""

        REAL:: A_c
        REAL:: A_j
        REAL:: A_p
        REAL:: A_n
        INTEGER:: a_n_limit_factor ! 0 = NA 1 = A_c 2 = A_j 3 = A_p
    end type

end module
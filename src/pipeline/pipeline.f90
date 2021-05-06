module pipeline
    ! use model_state
    ! use config
    ! use external_state
    implicit none

    ! public :: run_rows
    public :: hello
    contains
    ! pure TYPE(ModelState) Function run_rows(initial_state, config,external_state, start_day, end_day) result(final_state)

    !     TYPE(ModelState), intent(in):: initial_state
    !     TYPE(ConfigShape), intent(in):: config
    !     TYPE(ExternalStateShape), intent(in):: external_state
    !     INTEGER, intent(in):: start_day
    !     INTEGER, intent(in):: end_day

    !     final_state = initial_state
    ! end function

!     pure TYPE(ModelState) Function run_rows(initial_state) result(final_state)

!         TYPE(ModelState), intent(in):: initial_state

!         final_state = initial_state
! end function
    function hello(val_in) result(outval)
        REAL, intent(in):: val_in
        REAL :: outval
        outval = val_in + 1.0
    end function
end module pipeline

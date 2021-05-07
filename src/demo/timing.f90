module timing

    implicit none

    contains

    Pure Real Function runme(min, max)
        ! Elemental & Pure functions require intent declaration
        integer, Intent(in) :: min, max

        integer :: n

        real :: nfact

        nfact = 1.0

        do n = min, max
            IF (nfact < max) THEN
                nfact = nfact + n
            ELSE
                nfact = min
            ENDIF
        end do

        runme = nfact
    End Function

end module timing

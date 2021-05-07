module child

    implicit none
    public::foo


    TYPE:: Bar
        REAL:: a
    end type


    contains



    Pure Type(Bar) Function foo(x,y)
    ! Elemental & Pure functions require intent declaration
    real, Intent(in) :: x,y

        foo = Bar(x*y)

    End Function

    end module child

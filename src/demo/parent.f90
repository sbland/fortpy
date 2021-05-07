module parent

    use child
    implicit none

    contains



    Pure Real Function prodpure(x,y)
    ! Elemental & Pure functions require intent declaration
    real, Intent(in) :: x,y
    Type(Bar):: b
    b = foo(x, y)
    prodpure = b%a

    End Function

    end module parent

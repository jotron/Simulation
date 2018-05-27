from math import sqrt

"""Define method of Runge Kutta 4."""
def RK(f):
    return lambda t, y, dt: (
            lambda dy: (
            lambda dy: (
            lambda dy: (
            lambda dy: (dy + 2*(dy + dy) + dy)/6
                        )( dt * f( t + dt  , y + dy   ) )
	                    )( dt * f( t + dt/2, y + dy/2 ) )
	                    )( dt * f( t + dt/2, y + dy/2 ) )
	                    )( dt * f( t, y ) )

"""define function: y(t)"""
def y(t):
    return (y(t))

"""define function: y'(t) that applies RK(f)"""
dy = RK(lambda t, y: y/t)

"""define values for t0, y0, dt"""
t, y, dt = 1., 2., 1.

"""define number of while loop"""
while t <= 5:
        print("y(%0.1f)\t= %6.2f " % ( t, y))

        """define new values for y(t) and t to begin a new while loop"""
        t, y = t + dt, y + dy( t, y, dt )

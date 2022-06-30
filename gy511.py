import math
from cmath import pi


def gy511_inclinacion(acex,acez):
    angulo=complex(0,0)

    angulo = (math.atan2(acex,-acez)) *(180/pi)
    
    angulo=angulo.real

    if angulo <0:
        angulo = 360 + angulo


    return angulo

def gy511_azimut(magy,magx):


    azimut = (math.atan2(magy,-magx)) *(180/pi)
    
    azimut=azimut.real

    if azimut <0:
        azimut = 360 + azimut


    return azimut
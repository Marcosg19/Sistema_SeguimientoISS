import math
from cmath import pi

errorBrujula=25
def brujulacorregida(azimut):
    azimut= errorBrujula+azimut

    if (azimut>360):
        azimut=azimut-360
    return azimut


def gy511_inclinacion(acex,acez):
    angulo=complex(0,0)

    angulo = (math.atan2(acex,-acez)) *(180/pi)
    
    angulo=angulo.real

    if angulo <0:
        angulo = 360 + angulo


    return angulo

def gy511_azimut(magy,magx):


    azimut = (((math.atan2(magy,magx)) *(180))/3.1416)
    
    azimut=azimut.real

    if azimut <0:
        azimut = 360 + azimut

    if azimut<=180:
        azimut=180-azimut
    else:
        azimut=540-azimut

    azimut=brujulacorregida(azimut)

    return azimut
#control de stepper con board
#servo con adafruit
######################Brujula
import turtle
from turtle import *
import time
import board
import digitalio
import numpy as np
from collections import deque
import pwmio
#librerias del sensor
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
#libreria que calcula la inclinacion y el azimut
import gy511

def manual():
    def Compass():
        hideturtle()
        tracer(0, 0)
        global compasspointer
        global elevpointer
        penup()
        right(90)
        forward(90)
        left(90)
        pendown()
        circle(90)
        penup()
        home()
        color('green')
        goto(115, -15)
        write("0", font=('Arial', 15, 'normal'), align="center")
        home()
        goto(80, 65)
        write("45", font = ('Arial', 15, 'normal'), align="center")
        home()
        goto(0, 100)
        write("90", font = ('Arial', 15, 'normal'), align="center")
        home()
        goto(-80, 65)
        write("135", font = ('Arial', 15, 'normal'), align="center")
        home()
        goto(-115, -15)
        write("180", font = ('Arial', 15, 'normal'), align="center")
        home()
        penup()
        color('green')
        goto(-30, -50)
        write("Elevación", True, "left", ("Arial",12,"normal"))
        home()
        color('red')
        goto(-20, -120)
        write("Azimut", True, "left", ("Arial",12,"normal"))
        home()
        bgcolor('#E2DFDE')
        bgpic("brujula1.png")
        setup(500, 500)
        compasspointer = Turtle()
        compasspointer.degrees(360)
        compasspointer.home()
        compasspointer.settiltangle(0)
        compasspointer.shape("arrow")
        compasspointer.color("red")
        compasspointer.turtlesize(2, 18, 0)
        tracer(1, 1)
        compasspointer.speed()
        elevpointer = Turtle()
        elevpointer.degrees(360)
        elevpointer.home()
        elevpointer.settiltangle(0)
        elevpointer.shape("arrow")
        elevpointer.color("green")
        elevpointer.turtlesize(0.8, 9, 0)
        tracer(1, 1)
        elevpointer.speed()
        boton= Turtle()
        boton.hideturtle()
        boton.penup()
        boton.goto(-240, 220)
        boton.write("SALIR", font=("Arial",12,"normal"))
        def btnclick(x,y):
            if x > -240 and x < -159 and y > 220 and y < 245:
                quit()
        turtle.onscreenclick(btnclick,1)

    Compass()

    #########mecanismo#######################

    secuencia  = deque([1,0,0,0])


    ####Pines Stepper

    rojo= digitalio.DigitalInOut(board.D4)
    naranja= digitalio.DigitalInOut(board.D17)
    amarillo= digitalio.DigitalInOut(board.D18)
    azul= digitalio.DigitalInOut(board.D27)

    rojo.direction = digitalio.Direction.OUTPUT
    naranja.direction = digitalio.Direction.OUTPUT
    amarillo.direction = digitalio.Direction.OUTPUT
    azul.direction = digitalio.Direction.OUTPUT
    ####Pines Stepper

    ########

    ############servo motor #############
    # Initialize PWM output for the servo (on pin D5):
    servo = pwmio.PWMOut(board.D5, frequency=50)


    #inicializacion del sensor gy511 mide inclinacion y brujula


    i2c = busio.I2C(board.SCL, board.SDA)
    mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)





    # Create a function to simplify setting PWM duty cycle for the servo:
    def servo_duty_cycle(pulse_ms, frequency=50):
        period_ms = 1.0 / frequency * 1000.0
        duty_cycle = int(pulse_ms / (period_ms / 65535.0))
        return duty_cycle

    def _map(x, in_min, in_max, out_min, out_max):
        return float((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def servoAngle(angulo):
        angulo=_map(angulo,0,180,0.7,2.2)
        #print(angulo)
        servo.duty_cycle = servo_duty_cycle(angulo)
        time.sleep(1)
        servo.duty_cycle = servo_duty_cycle(0)


    #funcion para el motor stepper 
    def motorPasos(pasos,direccion,velocidad):

        for i in range(pasos):
            #print(list(secuencia), "  ", i)
            rojo.value= bool(secuencia[0])
            naranja.value= bool(secuencia[1])
            amarillo.value= bool(secuencia[2])
            azul.value= bool(secuencia[3])
            secuencia.rotate(direccion) #rotate right
            time.sleep(velocidad)
        


        #para apagarlo
        rojo.value= 0
        naranja.value= 0
        amarillo.value= 0
        azul.value= 0

    ##########################################

    velocidad=0.5
    direccion= -1 # -1   giro izquierda +1  giro a la derecha
    # pasos=10

    #motorPasos(10,direccion,velocidad)
    setInclinacion=0
    MsetInclinacion=0
    setAzimut=0
    horario=-1
    antihorario=1
    i=0
    errorInclinacion=360

    servoAngle(0)





    ######        end #########

    while True:
        
        time.sleep(0.4)

        Azimut=int(input("Introduzca el grado de azimut (entre 0 a 360): "))
        Elevacion=int(input("Introduzca el grado de elevacion (entre 0 a 180): "))
        
    ######################mecanismos#################################
    ##############################################

        #Elevacion= float(Elevacion)
        #Azimut = float(Azimut)
        #if Elevacion >5 and Elevacion<70:
        setInclinacion=Elevacion
        setAzimut=Azimut
        #else:
            #setInclinacion=0
            #setAzimut
        #print(setInclinacion,"    ", setAzimut)
        
        azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
        errorAzimut=int(azimut-setAzimut)
        compasspointer.settiltangle(-int(azimut)+90)

        # inclinacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
        # inclinacion= _map(inclinacion,0,360,360,0)
        # elevacion=inclinacion
        # errorInclinacion=int(inclinacion-setInclinacion)
        
                    #print(azimut)
        # elevpointer.settiltangle(int(elevacion))


        # if setInclinacion != MsetInclinacion:
        #     MsetInclinacion = setInclinacion
        #     if errorInclinacion<-2:
        #         servoAngle(setInclinacion)
        #         #i=i+1
        
        #     elif errorInclinacion>2:
        #         servoAngle(setInclinacion)
        #         #i=i-1
        #     # else:
        #     #     i=0
        
        
        #print("incli= ",inclinacion," error= ",errorInclinacion, "   valor= ",
        ################################
        #print("inclinacion = ",inclinacion,"azimut = ", azimut,"errorAzimut= ",errorAzimut)
        ############control del estepper#################
        while errorAzimut>1 or errorAzimut<-1:
            #azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
            
            ##############activa la brujula#################
            #compasspointer.settiltangle(-int(azimut)+90)
            inclinacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
            azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
            inclinacion= _map(inclinacion,0,360,360,0)
            errorAzimut=int(azimut-setAzimut)
            elevacion=inclinacion
            compasspointer.settiltangle(-int(azimut)+90)
                        #print(azimut)
            elevpointer.settiltangle(int(elevacion))

        
            ##############################################
            #errorAzimut=int(azimut-setAzimut)
            velocidad=_map(abs(errorAzimut),0,360,0.5,0.01)
            if errorAzimut>2 and errorAzimut<177:
                motorPasos(1,antihorario,velocidad) #antihorario
        
            if errorAzimut>180 and errorAzimut<355:
                motorPasos(1,horario,velocidad)
        
            if errorAzimut<-2 and errorAzimut>-177:
                motorPasos(1,horario,velocidad)
                #print("aqui3
            if errorAzimut<-180 and errorAzimut>-355:
                motorPasos(1,antihorario,velocidad)


        inclinacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
        inclinacion= _map(inclinacion,0,360,360,0)
        elevacion=inclinacion
        errorInclinacion=int(inclinacion-setInclinacion)


        elevpointer.settiltangle(int(elevacion))


        if setInclinacion != MsetInclinacion:
            MsetInclinacion = setInclinacion
            if errorInclinacion<-2:
                servoAngle(setInclinacion)
                #i=i+1
        
            elif errorInclinacion>2:
                servoAngle(setInclinacion)
                #i=i-1
            # else:
            #     i=0

        inclinacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
        inclinacion= _map(inclinacion,0,360,360,0)
        elevacion=inclinacion
        errorInclinacion=int(inclinacion-setInclinacion)


        elevpointer.settiltangle(int(elevacion))

    #############################end mecanismos   
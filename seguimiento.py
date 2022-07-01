import json
import math
import turtle
import urllib.request
import time
from datetime import datetime
import ephem
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


def isstiemporeal():

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

    ############servo motor #############
    # Initialize PWM output for the servo (on pin D5):
    servo = pwmio.PWMOut(board.D5, frequency=50)


    #inicializacion del sensor gy511 mide inclinacion y brujula


    i2c = busio.I2C(board.SCL, board.SDA)
    mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
    accel = adafruit_lsm303_accel.LSM303_Accel(i2c)


    #Crea una función para simplificar la configuración del ciclo de trabajo PWM para el servo:
    def servo_duty_cycle(pulse_ms, frequency=50):
        period_ms = 1.0 / frequency * 1000.0
        duty_cycle = int(pulse_ms / (period_ms / 65535.0))
        return duty_cycle

    def _map(x, in_min, in_max, out_min, out_max):
        return float((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def servoAngle(angulo):
        angulo=_map(angulo,0,180,0.7,2.4)
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

    ###### end #########

    elegir = turtle.Screen()

    menuprincipal = True
    while menuprincipal:
        opcion = elegir.numinput("Elegir opción", "Elegir opción:\n 1) Mapas\n 2) Brujula\n 3) Salir")
        if opcion==1:

            screen = turtle.Screen()
            iss = turtle.Turtle()
            iss.hideturtle()


            menu = True
            while menu:
                mapa = screen.numinput("Elegir mapa", "Elegir número de mapa:\n 1) Mapa 1\n 2) Mapa 2\n 3) Salir")
                if mapa==1:
                    screen.bgpic("mapa.gif")
                    screen.setup(1440, 720)
                    screen.setworldcoordinates(-180, -90, 180, 90)
                    screen.register_shape("issmapa1.gif")
                    iss.shape("issmapa1.gif")
                    iss.setheading(90)
                    iss.penup()
                    menu=False

                elif mapa==2:
                    screen.bgpic("mapa2.gif")
                    screen.setup(720, 360)
                    screen.setworldcoordinates(-180, -90, 180, 90)
                    screen.register_shape("issmapa2.gif")
                    iss.shape("issmapa2.gif")
                    iss.setheading(90)
                    iss.penup()
                    menu=False
                elif mapa==3:
                    print('Cerrando programa')
                    quit()
                else:
                    print("No es una opción valida")
                    menu=True


            while True:
                try:
                    #Carga el estado actual de la ISS en tiempo real
                    url = "http://api.open-notify.org/iss-now.json"
                    response = urllib.request.urlopen(url)
                    result = json.loads(response.read())

                    #Extrae la ubicación de la ISS
                    location = result["iss_position"]
                    lat = location['latitude']
                    lon = location['longitude']

                    #Salida lon y lat a la terminal
                    lat = float(lat)
                    lon = float(lon)
                    print("\nLatitud: " + str(lat))
                    print("\nLongitud: " + str(lon))
                    #Actualiza la ubicación de la ISS en el mapa
                    screen.title('Seguimiento de la ISS: (Latitud: '+ str(lat) +' Longitud: ' + str(lon) + ')')
                    iss.goto(lon, lat)
                    iss.dot()
                    degrees_per_radian = 180.0 / math.pi
                    home = ephem.Observer()
                    home.lon = '-90.5199'   # +E
                    home.lat = '14.6328'      # +N
                    #home.lon = '-56'   # +E
                    #home.lat = '52'      # +N               
                    home.elevation = 1489 # metros
                    iss1 = ephem.readtle('ISS',
                        '1 25544U 98067A   22181.49799769  .00007852  00000-0  14655-3 0  9990',
                        '2 25544  51.6442 270.6638 0004497 316.5381 218.6205 15.49775888347243'
                    )
                    home.date = datetime.utcnow()
                    iss1.compute(home)
                    Elevacion = '%4.1f' % (iss1.alt * degrees_per_radian)
                    Azimut =  '%5.1f' % (iss1.az * degrees_per_radian)
                    print('\n********************************************')
                    print('\nElevacion:', Elevacion ,', Azimut:', Azimut)
                    print('\n********************************************')
                    
                    guate = turtle.Turtle()
                    guate.penup()
                    guate.hideturtle()
                    cerco = turtle.Turtle()
                    cerco.hideturtle()
                    guate.goto(-90.5199,14.6328)
                    guate.color('white')
                    guate.write('Guatemala')
                    guate.dot()
                    cerco.penup()
                    cerco.goto(-90.5199, 5.5920815)
                    #cerco.goto(-90.519900000,23.666576300)
                    #cerco.dot()
                    #cerco.goto(-99.804286400, 14.917655600)
                    #cerco.dot()
                    #cerco.goto(-81.235513600, 14.917655600)
                    #cerco.dot()
                    #cerco.goto(-90.5199, 5.5920815)
                    #cerco.dot()
                    cerco.pendown()  
                    cerco.color('red')
                    cerco.circle(9)
                    texto= turtle.Turtle()
                    texto.penup()
                    texto.hideturtle()
                    texto.goto(-180, 76)
                    texto2= turtle.Turtle()
                    texto2.penup()
                    texto2.hideturtle()
                    texto2.goto(-180, -75)

                    if mapa==1:
                        texto.goto(-180, 78)
                        texto.color('white')
                        texto.write("Latitud= " + str(lat) + "\nLongitud=  " + str(lon), True, "left", ("Arial",12,"normal"))
                        texto2.goto(-180, -75)
                        texto2.color('white')
                        texto2.write("Azimut= " + str(Azimut) + "\nElevación=  " + str(Elevacion), True, "left", ("Arial",12,"normal"))
                    elif mapa==2:
                        texto.write("Latitud= " + str(lat) + "\nLongitud=  " + str(lon), True, "left", ("Arial",8,"normal"))
                        texto2.color('white')
                        texto2.write("Azimut= " + str(Azimut) + "\nElevación=  " + str(Elevacion), True, "left", ("Arial",9,"normal"))
                    #time.sleep(1)

    ######################mecanismos#################################
                    Elevacion= float(Elevacion)
                    Azimut = float(Azimut)

                    if Elevacion >5 :

                        setInclinacion=Elevacion
                        setAzimut=Azimut
                    else:
                        setInclinacion=0
                        setAzimut=0



                    print(setInclinacion,"    ", setAzimut)

                    
                    azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
                    
                    errorAzimut=int(azimut-setAzimut)

                    inclinacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
                    inclinacion= _map(inclinacion,0,360,360,0)
                    errorInclinacion=int(inclinacion-setInclinacion)

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
                    
                    
                    #print("incli= ",inclinacion," error= ",errorInclinacion, "   valor= ",i)

                    ################################
                    #print("inclinacion = ",inclinacion,"azimut = ", azimut,"errorAzimut= ",errorAzimut)
                    ############control del estepper###################

                    while errorAzimut>3 or errorAzimut<-3:



                        azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
                        ##############activa la brujula#################
                        #animabrujula.animaBrujula(int(azimut))
                        ##############################################
                        errorAzimut=int(azimut-setAzimut)
                        error1 = abs(errorAzimut)
                        if error1>180:
                            error1=360-error1

                        velocidad=_map(error1,0,180,0.4,0.01)


                        #velocidad=_map(abs(errorAzimut),0,360,0.5,0.01)
                        if errorAzimut>2 and errorAzimut<=180:
                            motorPasos(1,antihorario,velocidad) #antihorario
                    
                        if errorAzimut>180 and errorAzimut<=360 :
                            motorPasos(1,horario,velocidad)
                    
                        if errorAzimut<-2 and errorAzimut>=-180:
                            motorPasos(1,horario,velocidad)
                            #print("aqui3
                        if errorAzimut<-180 and errorAzimut>=-360:
                            motorPasos(1,antihorario,velocidad)

    #############################end mecanismos

                    texto.clear()
                    texto2.clear()

                    
                except Exception as e:
                    print(str(e))
                    quit()

        
        elif opcion==2:
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
                color('green')
                goto(115, -15)
                write("0", font=('Arial', 15, 'normal'), align="center")
                goto(80, 65)
                write("45", font = ('Arial', 15, 'normal'), align="center")
                goto(0, 100)
                write("90", font = ('Arial', 15, 'normal'), align="center")
                goto(-80, 65)
                write("135", font = ('Arial', 15, 'normal'), align="center")
                goto(-115, -15)
                write("180", font = ('Arial', 15, 'normal'), align="center")
                penup()
                color('green')
                goto(-30, -50)
                write("Elevación", True, "left", ("Arial",12,"normal"))
                color('red')
                goto(-20, -120)
                write("Azimut", True, "left", ("Arial",12,"normal"))
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
                compasspointer.speed(0)

                elevpointer = Turtle()
                elevpointer.degrees(360)
                elevpointer.home()
                elevpointer.settiltangle(0)
                elevpointer.shape("arrow")
                elevpointer.color("green")
                elevpointer.turtlesize(0.8, 9, 0)
                tracer(1, 1)
                elevpointer.speed(0)

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
            while (True):
                try:


                    degrees_per_radian = 180.0 / math.pi
                    home = ephem.Observer()
                    home.lon = '-90.5199'   # +E
                    home.lat = '14.6328'      # +N
                    #home.lon = '-45'   # +E
                    #home.lat = '50'      # +N               
                    home.elevation = 1489 # meters
                    iss1 = ephem.readtle('ISS',
                        '1 25544U 98067A   22181.49799769  .00007852  00000-0  14655-3 0  9990',
                        '2 25544  51.6442 270.6638 0004497 316.5381 218.6205 15.49775888347243'
                    )
                    home.date = datetime.utcnow()
                    iss1.compute(home)
                    Elevacion = '%4.1f' % (iss1.alt * degrees_per_radian)
                    Azimut =  '%5.1f' % (iss1.az * degrees_per_radian)
                    print('\n********************************************')
                    print('\nElevacion:', Elevacion ,', Azimut:', Azimut)
                    print('\n********************************************')
                    



                    elevacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
                    azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
                    elevacion= _map(elevacion,0,360,360,0)
                    #azimut = input("angulo= ")
                    #elevacion = input("angulo de elevación= ")
                    compasspointer.settiltangle(-int(azimut)+90)
                    #print(azimut)
                    elevpointer.settiltangle(int(elevacion))

    ######################mecanismos#################################
    ##############################################
                    Elevacion= float(Elevacion)
                    Azimut = float(Azimut)

                    if Elevacion >5 and Elevacion<70:

                        setInclinacion=Elevacion
                        setAzimut=Azimut
                    else:
                        setInclinacion=0
                        setAzimut=0



                    print(setInclinacion,"    ", setAzimut)

                    inclinacion=gy511.gy511_inclinacion(accel.acceleration[0],accel.acceleration[2])
                    azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
                    inclinacion= _map(inclinacion,0,360,360,0)
                    errorAzimut=int(azimut-setAzimut)


                

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
                    
                    errorInclinacion=int(inclinacion-setInclinacion)
                    #print("incli= ",inclinacion," error= ",errorInclinacion, "   valor= ",i)

                    ################################
                    #print("inclinacion = ",inclinacion,"azimut = ", azimut,"errorAzimut= ",errorAzimut)
                    ############control del estepper###################

                    while errorAzimut>3 or errorAzimut<-3:



                        azimut= gy511.gy511_azimut(mag.magnetic[1],mag.magnetic[0])
                        compasspointer.settiltangle(-int(azimut)+90)
                        #print(azimut)
                        #elevpointer.settiltangle(int(elevacion))
                        
                        ##############activa la brujula#################
                        #animabrujula.animaBrujula(int(azimut))
                        ##############################################
                        errorAzimut=int(azimut-setAzimut)
                        velocidad=_map(abs(errorAzimut),0,360,0.5,0.01)
                        if errorAzimut>2 and errorAzimut<177:
                            motorPasos(1,antihorario,velocidad) #antihorario
                        

                        if errorAzimut>180 and errorAzimut<355:
                            motorPasos(1,horario,velocidad)
                            

                        if errorAzimut<-2 and errorAzimut>-177:
                            motorPasos(1,horario,velocidad)
                            #print("aqui3")

                        if errorAzimut<-180 and errorAzimut>-355:
                            motorPasos(1,antihorario,velocidad)
            

    ##############################end macanismos 


                    #print(elevacion)
                except:
                    quit()

        elif opcion==3:
            print('Cerrando programa')
            quit()
        else:
            print("No es una opción valida")
            mapa=True
import json
import math
import turtle
import urllib.request
import time
import webbrowser
import geocoder
from datetime import datetime
import ephem
from turtle import *

def datosISS():
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    file = open("iss.txt", "w")
    file.write("Hay actualmente " +
            str(result["number"]) + " astronautas en la ISS: \n\n")
    people = result["people"]
    for p in people:
        file.write(p['name'] + " - a bordo" + "\n")

    g = geocoder.ip('me')
    file.write("\nTu latitud/longitud actual es: " + str(g.latlng))


    file.write('\n\n\nPredicciones de paso de ISS')
    # Latitud y Logitud de Guatemala
    latitud=14.6328
    longitud=-90.5199
    n=10 #número de veces que pasará la ISS


    Pass=('http://api.open-notify.org/iss-pass.json?lat={}&lon={}&n={}'.format(str(latitud),str(longitud),str(n)))
    response_Pass= urllib.request.urlopen(Pass)

    Pass_obj = json.loads(response_Pass.read())

    file.write('\n\n'+str(Pass_obj))

    pass_list=[]
    for count,item in enumerate(Pass_obj["response"], start=0):
        pass_list.append(Pass_obj['response'][count]['risetime'])
        file.write('\n\n'+datetime.fromtimestamp(pass_list[count]).strftime('%d-%m-%Y %H:%M:%S'))

    file.close()
    webbrowser.open("iss.txt")

def mapa():
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
                    screen.register_shape("issmapa12.gif")
                    iss.shape("issmapa12.gif")
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
                    #Cargando el estado actual de la ISS en tiempo real
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
                    #Actualizando la ubicación de la ISS en el mapa
                    screen.title('Seguimiento de la ISS: (Latitud: '+ str(lat) +' Longitud: ' + str(lon) + ')')
                    iss.goto(lon, lat)
                    iss.dot()
                    degrees_per_radian = 180.0 / math.pi
                    home = ephem.Observer()
                    home.lon = '-90.5199'   # +E
                    home.lat = '14.6328'      # +N
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
                    cerco.goto(-90.5199, 8.304786200)

                    cerco.goto(-90.519900000,20.957397300)
                    cerco.dot()
                    cerco.goto(-97.016650200,14.871316400)
                    cerco.dot()
                    cerco.goto(-84.023149800,14.871316400)
                    cerco.dot()
                    cerco.goto(-90.5199, 8.304786200)
                    cerco.dot()

                    cerco.pendown()  
                    cerco.color('red')
                    cerco.circle(6.5)
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
                    time.sleep(1)
                    texto.clear()
                    texto2.clear()
                except Exception as e:
                    print(str(e))
        
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
                #turtle.listen()
                #turtle.done()

            Compass()
            while (True):
                try:
                    azimut = input("Azimut= ")
                    elevacion = input("Elevación= ")
                    compasspointer.settiltangle(-int(azimut)+90)
                    print(azimut)
                    elevpointer.settiltangle(int(elevacion))
                    print(elevacion)
                except:
                    quit()
        elif opcion==3:
            print('Cerrando programa')
            quit()
        else:
            print("No es una opción valida")
            mapa=True

#datosISS()
#mapa()
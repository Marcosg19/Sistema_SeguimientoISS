import main 
import seguimiento
import manejomanual

def opciones():
    detenerop = False
    num = 0
    while not detenerop:
        try:
            detenerop = True    
            num = int(input('\nIngrese una opción: '))
        except ValueError:
            print('\nSeleccione una opción valida')
    return num

#Menú General
detenerprograma= True
while detenerprograma:
    print('\n-----------------------------------------------------------------------')
    print('|   Sistema de seguimiento de la estacion espacial internacional ISS  |')
    print('-----------------------------------------------------------------------')
    print('\nMENÚ')
    print('\n1. Manejo de mecanismo manualmente')
    print('2. Seguimiento de la ISS en tiempo real')
    print('3. Visualización de mapa y brújula')
    print('4. Datos de la ISS (Astronautas, Predicciones de paso)')
    print('5. Salir')

    opcionmenu = opciones()

    if opcionmenu == 1:
        manejomanual.manual()

    elif opcionmenu == 2:
        seguimiento.isstiemporeal()

    elif opcionmenu == 3:
        main.mapa()

    elif opcionmenu == 4:
        main.datosISS()

    elif opcionmenu == 5:
        print('\n>>>>>>CERRANDO PROGRAMA<<<<<<\n')
        detenerprograma = False

    else:
        print('\nIngrese una opción válida')
        input()
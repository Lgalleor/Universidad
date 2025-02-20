#menu de usuario, para poner todo en movimiento:
#vamos a tener dos opciones:
#    1. Vamos a ejecutar el codigo de guardar los datos de la baliza
#    2. Vamos a visualizar tanto los datos de la baliza como los del recorrido del dron

import os

def menu():
    while True:
        print("\n--- Menú de Monitoreo del Dron ---")
        print("1. Guardar nuevos datos de la baliza")
        print("2. Visualizar recorrido completo con los datos de la baliza")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            os.system("python Datos_baliza.py")
        elif opcion == '2':
            os.system("python Recorrido_baliza_dron.py")
        elif opcion == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    menu()

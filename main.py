import os
import msvcrt
from core import (
    analizar,
    agregar_palabra,
    palabras_positivas,
    palabras_negativas,
    saludos,
    identificacion,
    despedidas,
)

# Menu
while True:
    os.system("cls")
    print("1 - Analizar\n2 - Agregar palabras \n0 - Salir")
    entrada = input("Elija una opción: ").strip()
    if entrada == "1":
        while True:
            os.system("cls")
            print(
                "1 - Analizar 'audio_a_texto'\n2 - Analizar 'caso_de_ejemplo'\n3 - Analizar caso: cliente molesto\n4 - Analizar caso: agente alterado\n0 - Volver"
            )
            eleccion = input("Elija una opción: ").strip()
            if eleccion == "1":
                nombre_archivo = "audio_1_a_texto.txt"
                analizar(nombre_archivo)
            elif eleccion == "2":
                nombre_archivo = "caso_de_ejemplo_1.txt"
                analizar(nombre_archivo)
            elif eleccion == "3":
                nombre_archivo = "caso_de_ejemplo_2.txt"
                analizar(nombre_archivo)
            elif eleccion == "4":
                nombre_archivo = "caso_de_ejemplo_3.txt"
                analizar(nombre_archivo)
            elif eleccion == "0":
                os.system("cls")
                break

    elif entrada == "2":
        while True:
            os.system("cls")
            print("A qué conjunto de palabras desea agregar?")
            print(
                "1 - Palabras positivas\n2 - Palabras negativas\n3 - Saludos\n4 - Identificación del cliente\n5 - Despedidas\n0 - Volver"
            )
            eleccion = input("Elija una opción: ").strip()
            if eleccion == "1":
                while True:
                    palabra = input("Inserte una palabra: ").strip()
                    valor = input("Asigne un valor: ").strip()
                    if valor.isdigit() and not palabra.isdigit() and palabra != "":
                        agregar_palabra(palabras_positivas, palabra, int(valor))
                        print(f"Palabra '{palabra}' añadida con valor {valor}.")
                        print("Presione una tecla para continuar...")
                        msvcrt.getch()
                        break
            elif eleccion == "2":
                while True:
                    palabra = input("Inserte una palabra: ").strip()
                    valor = input("Asigne un valor: ").strip()
                    if valor.isdigit() and not palabra.isdigit() and palabra != "":
                        agregar_palabra(palabras_negativas, palabra, int(valor))
                        print(f"Palabra '{palabra}' añadida con valor {valor}.")
                        print("Presione una tecla para continuar...")
                        msvcrt.getch()
                        break
            elif eleccion == "3":
                while True:
                    palabra = input("Inserte una palabra: ").strip()
                    valor = ""
                    if not palabra.isdigit() and palabra != "":
                        agregar_palabra(saludos, palabra, valor)
                        print(f"Palabra '{palabra}' añadida.")
                        print("Presione una tecla para continuar...")
                        msvcrt.getch()
                        break
            elif eleccion == "4":
                while True:
                    palabra = input("Inserte una palabra: ").strip()
                    valor = ""
                    if not palabra.isdigit() and palabra != "":
                        agregar_palabra(identificacion, palabra, valor)
                        print(f"Palabra '{palabra}' añadida.")
                        print("Presione una tecla para continuar...")
                        msvcrt.getch()
                        break
            elif eleccion == "5":
                while True:
                    palabra = input("Inserte una palabra: ").strip()
                    valor = ""
                    if not palabra.isdigit() and palabra != "":
                        agregar_palabra(despedidas, palabra, valor)
                        print(f"Palabra '{palabra}' añadida.")
                        print("Presione una tecla para continuar...")
                        msvcrt.getch()
                        break
            elif eleccion == "0":
                os.system("cls")
                break
    elif entrada == "0":
        os.system("cls")
        break

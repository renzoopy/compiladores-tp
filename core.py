import os
import re
import msvcrt
from dictionaries import (
    palabras_positivas,
    palabras_negativas,
    saludos,
    identificacion,
    despedidas,
)


class Color:
    VERDE = "\033[32m"
    AMARILLO = "\033[33m"
    RESTABLECER = "\033[0m"


# 1. Leer el archivo de texto
def leer_transcripcion(nombre_archivo):
    ruta_archivo = os.path.join("texto", nombre_archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return archivo.readlines()


# 2. Separar diálogos por roles
def separar_dialogos(texto):
    agente = []
    cliente = []
    for linea in texto:
        if linea.startswith("Agente:"):
            agente.append(linea.replace("Agente:", "").strip())
        elif linea.startswith("Cliente:"):
            cliente.append(linea.replace("Cliente:", "").strip())
    return agente, cliente


# 3. Tokenizar las frases
def tokenizar(frases):
    tokens = []
    for frase in frases:
        # Separar palabras por espacios y remover signos de puntuación
        tokens += re.findall(r"\b\w+\b", frase.lower())
    return tokens


# 4. Analizar palabras clave
def analizar_palabras_clave(tokens):
    palabras_detectadas = {"positivas": [], "negativas": []}
    ponderacion_total = 0

    for token in tokens:
        if token in palabras_positivas:
            peso = palabras_positivas[token]
            palabras_detectadas["positivas"].append({token: peso})
            ponderacion_total += peso
        elif token in palabras_negativas:
            peso = palabras_negativas[token]
            palabras_detectadas["negativas"].append({token: peso})
            ponderacion_total += peso

    return palabras_detectadas, ponderacion_total


# 5. Verificar protocolo
def verificar_protocolo(agente_dialogos):
    protocolo = {
        "saludo": False,
        "identificacion_cliente": False,
        "despedida_amable": False,
        "palabras_positivas": [],
        "palabras_negativas": [],
        "ponderacion_sentimiento": 0,
    }

    # Calcular segmentos del diálogo
    inicio = int(len(agente_dialogos) * 0.4)  # 40% inicial
    final = int(len(agente_dialogos) * 0.7)  # 30% final
    inicio_dialogo = agente_dialogos[:inicio]
    final_dialogo = agente_dialogos[final:]

    # Tokenizar segmentos
    tokens_inicio = tokenizar(inicio_dialogo)
    tokens_final = tokenizar(final_dialogo)
    tokens_completos = tokenizar(agente_dialogos)

    # Verificar saludo e identificación en el 40% inicial
    protocolo["saludo"] = any(palabra in tokens_inicio for palabra in saludos)
    protocolo["identificacion_cliente"] = any(
        frase in " ".join(tokens_inicio) for frase in identificacion
    )

    # Verificar despedida amable en el 30% final
    protocolo["despedida_amable"] = any(
        frase in " ".join(tokens_final) for frase in despedidas
    )

    # Analizar palabras positivas y negativas
    palabras_detectadas, ponderacion_total = analizar_palabras_clave(tokens_completos)
    protocolo["palabras_positivas"] = palabras_detectadas["positivas"]
    protocolo["palabras_negativas"] = palabras_detectadas["negativas"]
    protocolo["ponderacion_sentimiento"] = ponderacion_total

    return protocolo


# 6. Obtener palabra más positiva
def obtener_mas_positiva(palabras_positivas):
    if not palabras_positivas:
        return None

    mas_positiva = max(
        palabras_positivas, key=lambda x: list(x.values())[0], default=None
    )
    return mas_positiva


# 7. Obtener palabra más negativa
def obtener_mas_negativa(palabras_negativas):
    if not palabras_negativas:
        return None

    mas_negativa = min(
        palabras_negativas, key=lambda x: list(x.values())[0], default=None
    )
    return mas_negativa


# 8. Impresión del protocolo de atención
def imprimir_protocolo_atencion(protocolo_agente):
    print("\n\tProtocolo de Atención")
    print(
        "Fase de saludo:",
        (
            (
                (Color.VERDE + "OK")
                if protocolo_agente.get("saludo")
                else (Color.AMARILLO + "Faltante")
            )
            + Color.RESTABLECER
        ),
    )
    print(
        "Identificación del cliente:",
        (
            (
                (Color.VERDE + "OK")
                if protocolo_agente.get("identificacion_cliente")
                else (Color.AMARILLO + "Faltante")
            )
            + Color.RESTABLECER
        ),
    )
    print(
        "Uso de palabras rudas: ",
        (
            (
                (Color.AMARILLO + "Detectadas")
                if protocolo_agente.get("palabras_negativas")
                else (Color.VERDE + "Ninguna detectada")
            )
            + Color.RESTABLECER
        ),
    )
    print(
        "Despedida amable:",
        (
            (
                (Color.VERDE + "OK")
                if protocolo_agente.get("despedida_amable")
                else (Color.AMARILLO + "Faltante")
            )
            + Color.RESTABLECER
        ),
    )


# 9. Impresión
def imprimir_deteccion_sentimiento(
    sentimiento_general,
    cantidad_palabras_positivas,
    palabra_mas_positiva,
    cantidad_palabras_negativas,
    palabra_mas_negativa,
):
    print("\n\tDetección de Sentimiento")
    print("Sentimiento general: ", sentimiento_general + Color.RESTABLECER)
    print(
        "Palabras positivas: ",
        Color.VERDE + f"{cantidad_palabras_positivas}" + Color.RESTABLECER,
    )
    if palabra_mas_positiva:
        palabra, peso = list(palabra_mas_positiva.items())[0]
        print(
            f"Palabra más positiva: {Color.VERDE}{palabra}, +{peso}{Color.RESTABLECER}"
        )
    else:
        print(f"Palabra más positiva: {Color.AMARILLO}No detectada{Color.RESTABLECER}")
    print(
        "Palabras negativas: ",
        Color.AMARILLO + f"{cantidad_palabras_negativas}" + Color.RESTABLECER,
    )
    if palabra_mas_negativa:
        palabra, peso = list(palabra_mas_negativa.items())[0]
        print(
            f"Palabra más negativa: {Color.AMARILLO}{palabra}, {peso}{Color.RESTABLECER}\n"
        )
    else:
        print(f"Palabra más negativa: {Color.VERDE}No detectada{Color.RESTABLECER}\n")


# 10. Agregar palabras a los dicionarios
def agregar_palabra(diccionario, palabra, valor):
    diccionario[palabra.lower()] = valor


# 11. Analizar texto
def analizar(nombre_archivo):
    texto = leer_transcripcion(nombre_archivo)
    agente_dialogos, cliente_dialogos = separar_dialogos(texto)

    # Análisis del agente
    protocolo_agente = verificar_protocolo(agente_dialogos)

    # Análisis del cliente
    tokens_cliente = tokenizar(cliente_dialogos)
    sentimiento_cliente, ponderacion_cliente = analizar_palabras_clave(tokens_cliente)

    # Análisis del sentimiento general de la conversación
    ponderacion_general = (
        protocolo_agente["ponderacion_sentimiento"] + ponderacion_cliente
    )
    if ponderacion_general > 0:
        sentimiento_general = Color.VERDE + f"Positivo (+{ponderacion_general})"
    elif ponderacion_general < 0:
        sentimiento_general = Color.AMARILLO + f"Negativo ({ponderacion_general})"
    else:
        sentimiento_general = f"Neutral (0)"

    # Cálculo de la cantidad de palabras positivas y negativas recogidas
    cantidad_palabras_positivas = len(sentimiento_cliente["positivas"]) + len(
        protocolo_agente["palabras_positivas"]
    )
    cantidad_palabras_negativas = len(sentimiento_cliente["negativas"]) + len(
        protocolo_agente["palabras_negativas"]
    )

    # Busqueda de palabra más positiva y más negativa
    palabra_mas_positiva = obtener_mas_positiva(
        protocolo_agente["palabras_positivas"] + sentimiento_cliente["positivas"]
    )
    palabra_mas_negativa = obtener_mas_negativa(
        protocolo_agente["palabras_negativas"] + sentimiento_cliente["negativas"]
    )

    # Impresión de resultados
    os.system("cls")
    # PROTOCOLO DE ATENCIÓN
    imprimir_protocolo_atencion(protocolo_agente)

    # DETECCIÓN DE SENTIMIENTO
    imprimir_deteccion_sentimiento(
        sentimiento_general,
        cantidad_palabras_positivas,
        palabra_mas_positiva,
        cantidad_palabras_negativas,
        palabra_mas_negativa,
    )

    print("Presione una tecla para continuar...")
    msvcrt.getch()
    os.system("cls")

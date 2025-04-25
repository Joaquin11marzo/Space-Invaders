import json
import os

RANKING_PATH = "ranking_general.json"  # Archivo de ranking

# Carga los datos del ranking desde el archivo
def cargar_ranking():
    if os.path.exists(RANKING_PATH):
        with open(RANKING_PATH, 'r') as f:
            return json.load(f)
    else:
        return []

# Guarda un nuevo puntaje y nombre en el ranking, sumando si ya existe
def guardar_ranking(nombre, puntaje):
    ranking = cargar_ranking()

    encontrado = False
    for entrada in ranking:
        if entrada['nombre'] == nombre:
            entrada['puntaje'] += puntaje
            encontrado = True
            break

    if not encontrado:
        ranking.append({"nombre": nombre, "puntaje": puntaje})

    ranking = sorted(ranking, key=lambda x: x['puntaje'], reverse=True)[:3]

    with open(RANKING_PATH, 'w') as f:
        json.dump(ranking, f)

# Devuelve el top 3 actual
def obtener_top_3():
    return cargar_ranking()

# Borra todo el ranking
def resetear_ranking():
    with open(RANKING_PATH, 'w') as f:
        json.dump([], f)
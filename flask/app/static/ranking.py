import json
from pymongo import MongoClient

def conectar_bd():
    client = MongoClient('mongodb+srv://gonzaloalv:5OrWE1buHSE3AjAP@tfg.acxkjkk.mongodb.net/')
    db = client['TFG']  # Reemplaza 'TFG' por el nombre de tu base de datos
    return db

def cargar_json(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def insertar_toda_informacion(json_data):
    db = conectar_bd()
    collection = db['ranking']  # Reemplaza 'tu_coleccion' por el nombre de tu colección

    # Verifica si ya hay datos en la colección
    if collection.count_documents({}) == 0:
        # Si la colección está vacía, inserta el JSON completo como un único documento
        collection.insert_one(json_data)
    else:
        # Si ya hay datos, realiza una actualización (puedes ajustar la lógica según tus necesidades)
        # En este ejemplo, se reemplaza el documento existente con el nuevo JSON
        collection.replace_one({}, json_data)

if __name__ == "__main__":
    ranking_json_path = 'ranking.json'  # Reemplaza con la ruta correcta del archivo ranking.json
    json_data = cargar_json(ranking_json_path)
    insertar_toda_informacion(json_data)

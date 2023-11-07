from google.cloud import translate_v2 as translate

# Configura las credenciales del servicio de Google Cloud Translation
client = translate.Client.from_service_account_json('ruta/a/tu/archivo-de-credenciales.json')

# Función para traducir un texto
def traducir_texto(texto):
    traduccion = client.translate(texto, target_language='es')  # Traduce al español
    return traduccion['input'], traduccion['translatedText']

# Lee el archivo de texto original
ruta_archivo_original = "C:/Users/gonza/Documents/IA/textos/progra_I.txt"  # Reemplaza con la ruta de tu archivo original

with open(ruta_archivo_original, "r", encoding="utf-8") as archivo_original:
    lineas_original = archivo_original.readlines()

# Traduce cada línea y guarda la traducción en un archivo
ruta_archivo_traducido = "C:/Users/gonza/Documents/IA/textos/progra_I_es.txt"  # Ruta para guardar el archivo traducido
with open(ruta_archivo_traducido, "w", encoding="utf-8") as archivo_traducido:
    for linea in lineas_original:
        _, linea_traducida = traducir_texto(linea)
        print(linea_traducida)
        archivo_traducido.write(linea_traducida + "\n")

print("Traducción completa. El archivo traducido se ha guardado en:", ruta_archivo_traducido)


import docx

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

# Ejemplo de uso
file_path = '/mnt/c/Users/gonza/Documents/IA/textos/progra_I.docx'  # Reemplaza esto con la ruta real de tu archivo .docx
extracted_text = extract_text_from_docx(file_path)

# Guardar el texto en un archivo .txt
output_file_path = 'progra_I.txt'  # Ruta para guardar el archivo .txt
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(extracted_text)

print(f'Texto extraído y guardado en: {output_file_path}')

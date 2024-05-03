import pymongo

def connect_to_mongodb(collection_name):
    """Conexión a la base de datos MongoDB y obtención de la colección."""
    client = pymongo.MongoClient("mongodb+srv://gelvin:gn*12862GN*003@ramselvin.lkxlmms.mongodb.net/?retryWrites=true&w=majority&appName=Ramselvin")
    db = client["datosco"]
    collection = db[collection_name]
    return collection

def insert_data(collection, data):
    """Insertar datos en la colección MongoDB."""
    result = collection.insert_many(data)
    print("Documentos insertados:", len(result.inserted_ids))
    
def update_data(collection, num_document, nuevas_causas):
    """
    Agregar nuevas causas al documento existente identificado por el numDocument dado.
    Si no existe un documento con ese numDocument, se insertará un nuevo registro.
    """
    # Buscar si existe un documento con el numDocument dado
    existing_document = collection.find_one({"numDocument": num_document})
    
    if existing_document:
        # Si el documento existe, agregar las nuevas causas sin eliminar las existentes
        query = {"numDocument": num_document}
        new_data = {"$addToSet": {"causas": {"$each": nuevas_causas}}}
        collection.update_one(query, new_data)
        print("Documento actualizado")
    else:
        # Si el documento no existe, insertar un nuevo registro con las causas proporcionadas
        data = {"numDocument": num_document, "causas": nuevas_causas}
        collection.insert_one(data)
        print("Nuevo documento insertado")
        
# Agregar lógica para registrar el proceso en la base de datos
def register_progress(document_number, page_number, total_pages, description, status):
    """
    Registra el proceso en la colección "proceso".
    
    Args:
        document_number (str): Número del documento.
        page_number (int): Número de la página actual.
        total_pages (int): Número total de páginas.
        description (str): Descripción del proceso.
        status (str): Estado del proceso (success, error, etc.).
    """
    # Obtener la colección "proceso" directamente
    collection = connect_to_mongodb("proceso")
    
    progress_data = {
        "document_number": document_number,
        "page_number": page_number,
        "total_pages": total_pages,
        "description": description,
        "status": status
    }
    collection.insert_one(progress_data)
    print("Proceso registrado:", progress_data)

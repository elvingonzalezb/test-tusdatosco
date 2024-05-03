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
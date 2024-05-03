def progressEntity(item) -> dict:
    return {
        "id": str(item.get('_id')),  # Si '_id' no está presente, devuelve None
        "document_number": str(item.get('document_number', '')),  # Si 'document_number' no está presente, devuelve una cadena vacía
        "page_number": item.get('page_number'),  # Si 'page_number' no está presente, devuelve None
        "total_pages": item.get('total_pages'),  # Si 'total_pages' no está presente, devuelve None
        "description": item.get('description', ''),  # Si 'description' no está presente, devuelve una cadena vacía
        "status": item.get('status', '')  # Si 'status' no está presente, devuelve una cadena vacía
    }

def progressesEntity(entity) -> list:
    # Empiezo a recorrer una lista y le paso el elemento a progressEntity para que genere el esquema
    return [progressEntity(item) for item in entity]

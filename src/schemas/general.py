def generalEntity(item) -> dict:    
    return {
        "id": str(item['_id']),
        "personType": str(item['personType']),
        "name": str(item['name']),
        "companyName": str(item['companyName']),
    }
    
def generalsEntity(entity) -> list:
    return [generalEntity(item) for item in entity]
    
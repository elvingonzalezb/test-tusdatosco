def causaEntity(item) -> dict:
    return {
        "id": str(item.get('_id')), 
        "numDocument": item.get('numDocument', ''), 
        "causas": [{
            "entryDate": causa.get('entryDate', ''),
            "numProcess": causa.get('numProcess', ''),
            "actionInfraction": causa.get('actionInfraction', ''),
            "idMovement": causa.get('idMovement', '')
        } for causa in item.get('causas', [])]
    }

def causasEntity(entity) -> list:
    return [causaEntity(item) for item in entity]
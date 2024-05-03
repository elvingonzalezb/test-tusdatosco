def userEntity(item) -> dict:
    return {
        #"id": str(item.get('_id')), 
        "username": str(item.get('username', '')),
        "email": item.get('email'),
        "password": item.get('password'),
        "status": item.get('status', 'initial')
    }

def usersEntity(entity) -> list:    
    return [usersEntity(item) for item in entity]

def userToken(item) -> dict:
    return {        
        "token": item.get('token')
    }


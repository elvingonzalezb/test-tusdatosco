from fastapi import APIRouter, status, Response
from src.config.db import db
from src.schemas.general import generalEntity, generalsEntity
from src.models.general import General
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from typing import List

general_router = APIRouter()

@general_router.get('/general', response_model=List[General], tags=["Generals"])
def find_all_general():
    """
    Finds all general entities from the MongoDB Atlas connection and returns their schemas.
    Returns:
    list: A list of schemas generated for each general entity found in the database.
    """
    return generalsEntity(db.datosco.general.find())

@general_router.post('/general', response_model=General, tags=["Generals"])
def create_general(general: General): # sourcery skip: avoid-builtin-shadow
    # convertimos en dictionary
    new_general = dict(general)
    
    id = db.datosco.general.insert_one(new_general).inserted_id
    general = db.datosco.general.find_one({"_id": id})
    return generalEntity(general)
    
@general_router.get('/general/{id}', response_model=General, tags=["Generals"])
def find_general(id: str):
    return generalEntity(db.datosco.general.find_one({"_id": ObjectId(id)}))

@general_router.put('/general/{id}', response_model=General, tags=["Generals"])
def update_general(id: str, general: General):
    db.datosco.general.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(general)}
    )
    return generalEntity(db.datosco.general.find_one({"_id": ObjectId(id)}))

@general_router.delete('/general/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Generals"])
def delete_general(id: str):
    db.datosco.general.find_one_and_delete({"_id": ObjectId(id)})
    return Response(status_code=HTTP_204_NO_CONTENT)

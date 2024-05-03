from fastapi import APIRouter, status, Response
from config.db import db
from schemas.proceso import progressEntity, progressesEntity
from models.proceso import Proceso
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from typing import List

proceso_router = APIRouter()

@proceso_router.get('/get', response_model=List[Proceso], tags=["Process"])
def find_all_proceso():
    """
    Finds all proceso entities from the MongoDB Atlas connection and returns their schemas.
    Returns:
    list: A list of schemas generated for each proceso entity found in the database.
    """
    return progressesEntity(db.datosco.proceso.find())
    
@proceso_router.get('/get/{id}', response_model=Proceso, tags=["Process"])
def find_proceso(id: str):
    return progressEntity(db.datosco.proceso.find_one({"_id": ObjectId(id)}))


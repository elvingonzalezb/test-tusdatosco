from fastapi import APIRouter, status, Response
from config.db import db
from schemas.causa import causaEntity, causasEntity
from models.causa import Causa
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from typing import List

causas_router = APIRouter()

@causas_router.get('/', response_model=List[Causa], tags=["Causas"])
def find_all_causas():
    """
    Finds all causas entities from the MongoDB Atlas connection and returns their schemas.
    Returns:
    list: A list of schemas generated for each causas entity found in the database.
    """
    return causasEntity(db.datosco.causas.find())

@causas_router.get('/{numDcocument}', response_model=Causa, tags=["Causas"])
def find_causa_by_num_document(numDcocument: str):
    return causaEntity(db.datosco.causas.find_one({"numDocument": numDcocument}))

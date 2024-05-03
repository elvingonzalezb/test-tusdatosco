from fastapi import APIRouter, status, Response, HTTPException, Depends
from config.db import db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from schemas.user import userEntity, usersEntity, userToken
from models.user import User, UserOut, UserAuth, TokenSchema, UserToken
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from typing import List
from utils.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token
)
from uuid import uuid4

user_router = APIRouter()

# @user_router.get('/get', response_model=List[User], tags=["Auth"])
# def find_all_users():
#     """
#     Finds all user entities from the MongoDB Atlas connection and returns their schemas.
#     Returns:
#     list: A list of schemas generated for each user entity found in the database.
#     """
#     return usersEntity(db.datosco.user.find())
    
# Tu endpoint para buscar usuario
@user_router.get('/user/me', response_model=UserToken, tags=["Auth"])
def find_user():
    return userToken(db.datosco.user.find_one({"email": 'ing.elvingonzalez@gmail.com'}))

# @user_router.post('/', response_model=User, tags=["Auth"])
# def create_user(user: User):
#     new_user = dict(user)
    
#     newUserId = db.datosco.user.insert_one(new_user).inserted_id
#     user = db.datosco.user.find_one({"_id": newUserId})
#     return userEntity(user)

@user_router.post('/signup', summary="Create new user", response_model=User, tags=["Auth"])
async def create_user(data: User):    
    userExist = db.datosco.user.find_one({"email": data.email})
    if userExist is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    new_user = {
        'email': data.email,
        'username': data.username,
        'password': get_hashed_password(data.password),
        'id': str(uuid4()),
        'status': 'verified',
        'token': create_access_token(data.email)
    }
    
    newUserId = db.datosco.user.insert_one(new_user).inserted_id
    new_user = db.datosco.user.find_one({"_id": newUserId})
    return userEntity(new_user)

@user_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):    
    user = db.datosco.user.find_one({"email": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    # Verificar si el token existe y es válido
    if 'token' in user and verify_token(user['token']):
        return {
            "access_token": user['token'],  # Utilizar el token existente si es válido
            "refresh_token": create_refresh_token(user['email'])
        }
    else:
        # Si el token no es válido o no existe, crear uno nuevo
        return {
            "access_token": create_access_token(user['email']),
            "refresh_token": create_refresh_token(user['email']),
        }

@user_router.get("/", tags=["Auth"])
async def root():
    return {"message": "Application for test Tus Datosco"}
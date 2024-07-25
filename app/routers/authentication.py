from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Tokens)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="User Credential did not Match")
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="User Credential did not Match")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # create Token and return Token
    return {"access_token": access_token, "token_type": "bearer"}

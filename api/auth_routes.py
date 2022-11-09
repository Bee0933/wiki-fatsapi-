from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db import SessionLocal, User
from .schema import signUser, logUser, Settings

# create auth router instance for sign-up and log-in
auth_route = APIRouter(prefix="/auth", tags=["AUTH"])

# JWT config
@AuthJWT.load_config
def get_config():
    return Settings()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# signin route
@auth_route.post("/sign-in", status_code=status.HTTP_201_CREATED)
async def sigin(user: signUser, db: Session = Depends(get_db)):
    # query db if email exists
    db_email = db.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user email already exists"
        )

    # query db if username exists
    db_username = db.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists"
        )

    # create new user to ingest to database
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
    )

    db.add(new_user)

    db.commit()
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


# login route
@auth_route.post("/log-in", status_code=status.HTTP_201_CREATED)
async def login(
    user: logUser, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    # query db if user exists
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user and check_password_hash(db_user.password, user.password):

        # create jwt access token for authorized user
        access_token = Authorize.create_access_token(subject=db_user.username)

        # create refresh token for authorized user
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        # output response
        response = {"access token": access_token, "refresh token": refresh_token}
        return jsonable_encoder(response)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
    )


# refresh route
@auth_route.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        # request access token from authorized user
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="please provide a valid refresh token",
        ) from e

    current_user = Authorize.get_jwt_subject()
    # print('current_user:', current_user)

    # create new token for authorized user
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access token": access_token})


# pylint: disable=redefined-builtin
# get single user
@auth_route.get("/{id}", status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    response = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
    }
    return jsonable_encoder(response)

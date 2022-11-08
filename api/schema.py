# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import BaseModel, Field, EmailStr
from decouple import config


# wiki search key
class key_search(BaseModel):
    key: str = Field(default=None, description="search keyword")


# wiki search title
class page_search(BaseModel):
    title: str = Field(default=None, description="search pages")


# sign-in end-point schema
class signUser(BaseModel):
    username: str = Field(default=None, max_length=30, description="user unique name")
    email: EmailStr = Field(default=None, description="user email for log-in")
    password: str = Field(default=None, description="user password for log-in")

    class config:
        orm_mode = True
        schema_extra = {
            "username": "<username>",
            "email": "<user@email.com>",
            "password": "<password>",
        }


# log-in end-point schema
class logUser(BaseModel):
    email: EmailStr = Field(default=None, description="user email to log-in")
    password: str = Field(default=None, description="user password for log-in")

    class config:
        orm_mode = True
        schema_extra = {
            "email": "<user@email.com>",
            "password": "<password>",
        }


# jwt auth
class Settings(BaseModel):
    authjwt_secret_key: str = config("secret")
    authjwt_access_token_expires: int = 1800  # 30 minutes
    authjwt_refresh_token_expires: int = 1800  # 30 minutes

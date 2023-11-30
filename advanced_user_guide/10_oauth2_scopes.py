# https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
# In this section you will see how to manage authentication and authorization with the same OAuth2 with scopes in your FastAPI application.

"""

This is a more or less advanced section. If you are just starting, you can skip it.

You don't necessarily need OAuth2 scopes, and you can handle authentication and authorization however you want.

But OAuth2 with scopes can be nicely integrated into your API (with OpenAPI) and your API docs.

Nevertheless, you still enforce those scopes, or any other security/authorization requirement, however you need, in your code.

In many cases, OAuth2 with scopes can be an overkill.

But if you know you need it, or you are curious, keep reading.

"""

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

# jwt
SECRET_KEY = "a0e65ff0d9ba48989f09eb385ea4290676695cfaadd943be992aacad7c74aba6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class User(BaseModel):
    usernmae: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_contenxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items",
    },  # The scopes parameter receives a dict with each scope as a key and the description as the value:
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    pwd_contenxt.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_contenxt.hash(password)


def get_user(db: dict, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db: dict, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = timedelta(minutes=15)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},  # this is part of the spec
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(socpes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credential_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credential_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])]
):
    """
    the scope "me" declared at get_current_active_user will be included in the list of required scopes in the security_scopes.scopes passed to get_current_user.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Iactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={
            "sub": user.username,
            "scopes": form_data.scopes,
        },  # OAuth2PasswordRequestForm. It includes a property scopes with a list of str, with each scope it received in the request.
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    security_scopes.scopes will contain ["me"] for the path operation read_users_me, because it is declared in the dependency get_current_active_user.
    """
    return current_user


@app.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["items"])
    ]  # (just like Depends), but Security also receives a parameter scopes with a list of scopes (strings).
):
    """
    Now we declare that the path operation for /users/me/items/ requires the scope items.

    ** security_scopes.scopes will contain ["me", "items"] for the path operation read_own_items.
    """
    return [{"item_id": "Food", "owner": current_user.usernmae}]


@app.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    """
    security_scopes.scopes will contain [] (nothing) for the path operation read_system_status,
    because it didn't declare any Security with scopes, and its dependency, get_current_user, doesn't declare any scope either.
    """
    return {"status": "ok"}

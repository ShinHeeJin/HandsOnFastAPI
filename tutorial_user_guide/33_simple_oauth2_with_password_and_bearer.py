# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
# OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password fields as form data.

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str) -> str:
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(  # here is also part of the spec.
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_activate_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    OAuth2PasswordRequestForm is a class dependency that declares a form body with:

    - The username.
    - The password.
    - An optional scope field as a big string, composed of strings separated by spaces.
    - An optional grant_type.
    - An optional client_id.
    - An optional client_secret.

    tip. If you need to enforce grant_type(OAuth2 spec), use OAuth2PasswordRequestFormStrict instead of OAuth2PasswordRequestForm.
    """
    # user_dict = {'username': 'alice', 'full_name': 'Alice Wonderson', 'email': 'alice@example.com', 'hashed_password': 'fakehashedsecret2', 'disabled': True}
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # UserInDB(username='alice', email='alice@example.com', full_name='Alice Wonderson', disabled=True, hashed_password='fakehashedsecret2')
    user = UserInDB(**user_dict)

    # hashed_password = 'fakehashedsecret3'
    hashed_password = fake_hash_password(form_data.password)
    if not (hashed_password == user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    """
    It should have a token_type. In our case, as we are using "Bearer" tokens, the token type should be "bearer".
    And it should have an access_token, with a string containing our access token.
    """
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_activate_user)]):
    return current_user

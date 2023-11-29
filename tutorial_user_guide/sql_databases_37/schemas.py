from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        """
        This Config class is used to provide configurations to Pydantic.
        You will be able to return a database model and it will read the data from it.

        UserWarning: Valid config keys have changed in V2:
        * 'orm_mode' has been renamed to 'from_attributes'
        """

        from_attributes = True
        # orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_model = True

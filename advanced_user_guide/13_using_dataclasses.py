from dataclasses import dataclass, field

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: str | None = None
    tax: float | None = None


app = FastAPI()


# Using Dataclasses
@app.post(
    "/items/",
    response_model=Item,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {"name": "item", "price": 10.5, "description": "my item", "tax": 0.5}
                }
            },
            "description": "description of items",
        }
    },
)
async def create_item(item: Item):
    """
    This is still supported thanks to Pydantic, as it has internal support for dataclasses.
    So, even with the code above that doesn't use Pydantic explicitly,
    FastAPI is using Pydantic to convert those standard dataclasses to Pydantic's own flavor of dataclasses.
    """
    return item


@dataclass
class Item2:
    name: str
    description: str | None = None


@dataclass
class Author:
    name: str
    items: list[Item2] = field(default_factory=list)


# Dataclasses in Nested Data Structures
@app.post("/authors/{author_id}/items/", response_model=Author)  #
async def create_author_items(author_id: str, items: list[Item2]):  #
    return {"name": author_id, "items": items}  #


@app.get("/authors/", response_model=list[Author])  #
def get_authors():  #
    return [  #
        {
            "name": "Breaters",
            "items": [
                {
                    "name": "Island In The Moon",
                    "description": "A place to be be playin' and havin' fun",
                },
                {"name": "Holy Buddies"},
            ],
        },
        {
            "name": "System of an Up",
            "items": [
                {
                    "name": "Salt",
                    "description": "The kombucha mushroom people's favorite",
                },
                {"name": "Pad Thai"},
                {
                    "name": "Lonely Night",
                    "description": "The mostests lonliest nightiest of allest",
                },
            ],
        },
    ]

# https://fastapi.tiangolo.com/tutorial/sql-databases
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from tutorial_user_guide.sql_databases_37.database import engine, SessionLocal
from tutorial_user_guide.sql_databases_37 import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """
    Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the request is finished.
    We make sure the database session is always closed after the request. Even if there was an exception while processing the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    We are creating the database session before each request in the dependency with yield, and then closing it afterwards.
    And then we can create the required dependency in the path operation function, to get that session directly.
    With that, we can just call crud.get_user directly from inside of the path operation function and use that session.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

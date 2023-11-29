# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/

# FastAPI supports dependencies that do some extra steps after finishing.
from dataclasses import dataclass


@dataclass
class DBSession:
    closed: bool = True

    def close(self):
        self.closed = True


# A dependency with yield and try
async def get_db():
    """
    you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.
    """
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

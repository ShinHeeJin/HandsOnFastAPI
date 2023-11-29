# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
# FastAPI supports dependencies that do some extra steps after finishing.
# To do this, use yield instead of return, and write the extra steps after.

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI


@dataclass
class DBSession:
    name: str
    closed: bool = False

    def close(self):
        print(f"{self.name} session is closed")
        self.closed = True


# A dependency with yield and try
async def get_db():
    """
    you can use finally to make sure the exit steps are executed, no matter if there was an exception or not.
    """
    db = DBSession()
    try:
        yield db  # `The yielded value is what is injected into path operations` and other dependencies:

    finally:  # The code following the yield statement is executed `after the response` has been delivered:
        db.close()


app = FastAPI()


async def generate_dep(name):
    return DBSession(name)


async def dependency_a():
    print("dependency_a")
    dep_a = generate_dep("a")
    try:
        print("a yield")
        yield dep_a
    finally:
        print("a close")
        dep_a.close()


async def dependency_b(dep_a: Annotated[DBSession, Depends(dependency_a)]):
    print("dependency_b")
    dep_b = generate_dep("b")
    try:
        print("b yield")
        yield dep_b
    finally:
        print("b close")
        dep_b.close()


async def dependency_c(dep_b: Annotated[DBSession, Depends(dependency_b)]):
    """
    It might be tempting to raise an HTTPException or similar in the exit code, after the yield. But it won't work.
    """
    print("dependency_c")
    dep_c = generate_dep("c")
    try:
        print("c yield")
        yield dep_c
    finally:
        print("c close")
        dep_c.close()


# Sub-dependencies with yield
@app.get("/dependency-test")
async def dependency_test(dep_c: Annotated[str, Depends(dependency_c)]):
    """
    Log

    dependency_a
    a yield
    dependency_b
    b yield
    dependency_c
    c yield
    dep_c=<coroutine object generate_dep at 0x1107c92f0>

    INFO:     127.0.0.1:50446 - "GET /dependency-test HTTP/1.1" 200 OK
    c close
    b close
    a close
    """
    print(f"{dep_c=}")
    return None

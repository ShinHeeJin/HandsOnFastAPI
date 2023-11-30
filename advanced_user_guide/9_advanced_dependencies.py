from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


# A "callable" instance
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    """
    Request : http://127.0.0.1:8000/query-checker?q=bartest
    Response : {"fixed_content_in_query": true}
    """
    return {"fixed_content_in_query": fixed_content_included}

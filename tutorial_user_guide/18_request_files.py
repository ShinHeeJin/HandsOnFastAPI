from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


# Define File Parameters
@app.post("/file/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes", title="Title")] = None):
    if not file:
        return {"message": "No file sent"}
    return {"file_size": len(file)}


# File Parameters with UploadFile
@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    """
    ### 1. Using UploadFile has several advantages over bytes:

    1. You don't have to use File() in the default value of the parameter.
    2. It uses a "spooled" file:
        * A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
    3. This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.

    ### 2. UploadFile has the following async methods.
    As all these methods are async methods, you need to "await" them.

    ```python
    content = await file.read()
    ```
    """
    print(f"{type(file)=}")  # =<class 'starlette.datastructures.UploadFile'>
    if not file:
        return {"message": "No upload file sent"}
    return {"filename": file.filename}


# Multiple File Uploads
@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"file_sizes": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
        <body>
        <form action="/files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)

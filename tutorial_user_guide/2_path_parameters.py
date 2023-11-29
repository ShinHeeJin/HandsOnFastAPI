from enum import Enum

from fastapi import FastAPI


class ModelName(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


# Using Enum
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(f"{type(model_name)}")  # <enum 'ModelName'>

    if model_name is ModelName.alexnet:
        return {"model_name is alexnet"}
    if model_name.value == "lenet":
        return "model_name is lenet"

    return ["model_name is resnet"]


# Using Path by `:path` ( like file path )
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    Request : http://127.0.0.1:8000/files//home/user
    Response : {"file_path": "/home/user"}
    """
    return {"file_path": file_path}

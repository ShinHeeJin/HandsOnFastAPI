from enum import Enum

from fastapi import FastAPI


class ModelName(Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(f"{type(model_name)}")  # <enum 'ModelName'>

    if model_name is ModelName.alexnet:
        return {"model_name is alexnet"}
    if model_name.value == "lenet":
        return "model_name is lenet"

    return ["model_name is resnet"]

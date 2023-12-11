# For example, a database connection pool, or loading a shared machine learning model.
# That's what we'll solve, let's load the model before the requests are handled
# but only right before the application starts receiving requests, not while the code is being loaded.

from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everythin_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    That's what we'll solve, let's load the model before the requests are handled
    but only right before the application starts receiving requests
    not while the code is being loaded.
    """
    ml_models["answer_to_everything"] = fake_answer_to_everythin_ml_model
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}

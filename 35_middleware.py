# https://fastapi.tiangolo.com/tutorial/middleware/
# If you have dependencies with yield, the exit code will run after the middleware.
# If there were any background tasks (documented later), they will run after all the middleware.


import time

from fastapi import FastAPI, Request

app = FastAPI()


# create middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

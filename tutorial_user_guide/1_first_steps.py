from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# 위에 이미 items/{item_id} url이 지정되어 있기 때문에 /items/me은 호출될 수 없다.
# 이를 구현하기위해서 view 함수 를 read_item 함수보다 먼저(위쪽에) 정의해야 한다.
@app.get("/items/me")
async def read_me_item():
    return {"item_id": "me"}

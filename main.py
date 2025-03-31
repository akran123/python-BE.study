from fastapi import FastAPI   #모듈 가져오기
from typing import Union
from pydantic import BaseModel

app = FastAPI()    # app 객체 생성

# 서버 호출 uvicorn main:app --reload

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]




@app.get("/")  # 경로 아래에 있는 함수가 다음으로 이동하는 요청을 처리
async def root():
    return {"message": "Hello World"}



# 경로 파라미터터
@app.get("/users/{user_id}")   
def get_user(user_id: int ):   # int로 타입 지정(다른 타입시 오류 발생) fastapi가 내부적으로 자동 유효성 검사해줌
    return {"user_id": user_id}


#쿼리 파라미터
@app.get("/items/")  # 경로 매개변수 인자 이외의 추가 인자는 쿼리파라미터터
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):  # q가 선택적으로 대입할 수 있게 해줌 기본값 none 설정
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}





'''
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    '''

class Item(BaseModel):    # 지금은 모델로 하지만 사실 모델은 데이터베이스 저장용이며 응답요청 검증은 schema로 함
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

'''
요청의 본문을 JSON으로 읽어 들임
대응되는 타입으로 변환
데이터를 검증
'''
# 모델 사용
@app.post("/items/")
async def create_item(item: Item): # 위의 모델 기준으로 들어오는 데이터만 허용
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

@app.put("/items/{item_id}/123")  # /123을 지울 시 위에랑 충돌이 남(fastapi는 위 우선)
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

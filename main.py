from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel

# 데이터 모델 정의
class PerformanceEntry(BaseModel):
    category: str
    meta: str
    value: float
    time: datetime = None  # 자동으로 시간을 설정

app = FastAPI(title="Performance Beacon")

# MongoDB 클라이언트 설정
client = MongoClient("mongodb://hanslab.org:57017/")
db = client.performance_data
collection = db.metrics

# 성능 데이터 수집 엔드포인트
@app.post("/collect/")
async def collect_performance_data(entry: PerformanceEntry):
    entry.time = datetime.now()  # 현재 시간 자동 추가
    collection.insert_one(entry.dict())
    return {"message": "Data collected successfully"}

# 데이터 검색 엔드포인트
@app.get("/search/")
async def search_performance_data(category: str, meta: str):
    results = collection.find({"category": category, "meta": meta})
    result_list = list(results)
    if not result_list:
        raise HTTPException(status_code=404, detail="No data found")
    return {"val":[x['value'] for x in result_list]}    
    
# 서버 실행하기
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

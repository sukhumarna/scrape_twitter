from fastapi import FastAPI, status
from app.routers import tweets

app = FastAPI(
    title="Twitter Service"
)
app.include_router(tweets.router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck():
    return {"status": 'OK'}
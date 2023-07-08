# API endpoint
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root(user_id: int):
    return {"message": f"Hello {user_id}"}

if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
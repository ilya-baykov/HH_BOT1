from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()


@app.get("/callback")
async def callback(request: Request):
    # Получаем параметры из URL
    query_params = request.query_params
    code = query_params.get("code")
    state = query_params.get("state")

    if not code:
        return JSONResponse(content={"error": "Authorization failed. No code provided."}, status_code=400)

    # Возвращаем ответ
    return {"message": "Authorization successful!", "code": code, "state": state}

# uvicorn.run(app, host="localhost", port=3000) # Запуск сервера

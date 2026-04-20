from fastapi import FastAPI
from app.api.endpionts import auth, proxy, ws, users
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Proxy Service API")

#TODO исправить потом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Для тестов можно так
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(proxy.router, prefix="/api/proxy", tags=["proxy"])
app.include_router(ws.router, tags=["websocket"])

app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Proxy Service API"}
from fastapi import FastAPI
from routers import news, user,favorite,history
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],     # 允许的请求方法
    allow_headers=["*"],     # 允许的请求头
)



app.include_router(news.router)
app.include_router(user.router)
app.include_router(favorite.router)
app.include_router(history.router)

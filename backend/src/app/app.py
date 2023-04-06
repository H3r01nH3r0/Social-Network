from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.auth.router import router as auth_router
from src.app.posts.router import router as posts_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(auth_router)
app.include_router(posts_router)
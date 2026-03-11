from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, schemas
from .api import auth, profile, recommend, grade, chat

app = FastAPI(title="Python Edition API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    database.init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(grade.router, prefix="/grade", tags=["grade"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/health")
def health():
    return {"status": "ok"}

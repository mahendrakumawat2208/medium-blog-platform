from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import engine, Base
from app.api import auth, users, posts, feed

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.project_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(posts.router, prefix=settings.api_v1_prefix)
app.include_router(feed.router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return {"message": "Folio Blog API", "docs": "/docs"}

from fastapi import FastAPI
# from . import models
# from .database import engine
from .routers import post
from .routers import user
from .routers import auth
from .routers import vote
from fastapi.middleware.cors import CORSMiddleware

# DOCUMENTATION -----------------
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/redoc
# uvicorn app.main:app --reaload


# Commented because alembic does all the job
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# import all the @router objects
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Message for
@app.get("/")
def root():
    return {"message": "Hello World DEPLOYED!!!!"}

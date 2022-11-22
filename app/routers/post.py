from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
# import sys
# sys.path.append('.')
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/posts",
    # Documentation title
    tags=['Posts']
)


# @app is the decorator that calls FastAPI
# get for the HTTP method
# "/" represents the path of the URL (after the 127.0.0.1:8000) f.e: "/posts" means 127.0.0.1:8000/posts
# if two functions have a similar path, it will take the first one. Order matters.
# every change requires to stop the re run the server except uvicorn main:app --reload (only in development env)
# @router.get("/")
# def root():
#     return {"message": "Welcome to my API!"}


# CREATE -------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# that's the way to change the default status code
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):  # instance of Post class
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    # convert post schema to a regular dictionary. It's equivalent of previous statement
    # also add the current_user.id as the owner_id
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
# title str, content str


# GET -------------------
# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
# List from typing library because response is more than 1 result
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # ------------ All posts no matter who is logged in ----------------
    # post_query = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # JOIN by default is an inner join
    result = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # ------------ All posts from user who is logged in ----------------
    # To filter posts by current_user.id
    # post_query = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return result


# if this was after @app.get("/posts/{id}") it would not work because order matters and "/latest"
# would be consider equivalent to "/{id}" so the program would run that function
# @router.get("/{post_id}", response_model=schemas.PostResponse)
@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # automatically convert it to int to avoid errors
    # post_query = db.query(models.Post).filter(models.Post.id == post_id).first()

    # JOIN by default is an inner join
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == post_id).first()

    if not post_query:
        # change the status code to show 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} was not found")

    # OPTIONAL To check if the user trying to update is the owner
    # if post_query.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this action')

    return post_query


# DELETE -------------------
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} does not exists")

    # To check if the user trying to delete is the owner
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # it is supposed not to send data back after 204


# UPDATE -------------------
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} does not exists")

    # To check if the user trying to update is the owner
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform this action')

    # Convert the updated_post to dictionary to update the post
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

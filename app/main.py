from fastapi import FastAPI, status, HTTPException, Response, Depends
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import Post, PostResponse
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# get all the posts
@app.get("/")
def root():
    return {"message": "Hello world!"}


# get all the posts
@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


# create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get one post
@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    selected_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not selected_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )
    return selected_post


# delete one post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post
@app.put("/posts/{id}", response_model=PostResponse)
def update_posts(id: int, updated_post: Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

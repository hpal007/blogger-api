from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randint, randrange

from pydantic.networks import HttpUrl

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1,
    },
    {
        "title": "Fav foods",
        "content": "content of post 1",
        "id": 2,
    },
]


def find_post(id):
    for el in my_posts:
        if el.get("id") == id:
            return el


def get_index(id):
    for el in my_posts:
        if el.get("id") == id:
            index = my_posts.pop(my_posts.index(el))
            return index


# get all the posts
@app.get("/")
def read_root():
    return my_posts


# create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# get one post
@app.get("/posts/{id}")
def get_post(id: int):
    data = find_post(id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with {id} not found."}
    return {"data": data}


# delete one post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = get_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

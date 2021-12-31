from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randint, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from starlette.routing import Host
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="12345678",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succesfull!!")
        break
    except Exception as error:
        print(f"Connection failed with error: {error}")
        time.sleep(2)


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
    {
        "title": "New Post in the list",
        "content": "I need to complete atlest 1 hour today.",
        "id": 3,
    },
]


def find_post(id):
    for el in my_posts:
        if el.get("id") == id:
            return el


def get_index(id):
    for index, obj in enumerate(my_posts):
        if obj.get("id") == id:
            return index


# get all the posts
@app.get("/")
def read_root():
    return my_posts


# get all the posts
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"data": posts}


# create new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# get one post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""select * from posts where id = %s """, (str(id),))
    selected_post = cursor.fetchone()
    if not selected_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )
    return {"data": selected_post}


# delete one post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts where id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update post
@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cursor.execute(
        """ Update posts SET title =%s, content=%s,published=%s WHERE id = %s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Post with {id} not found."},
        )

    return {"data": updated_post}

# FastAPI development log

## 31122021

    ## Added
    update API endpoint
    Added psycopg2==2.9.3 and replaced hardcoded dictionary with postgres database.
    Added database.py for SQLAlchemy configuration.
    @11:20PM
    Added models.py to use ORM for creating tables
    updated database.py with get_db function to connect postgres db with session.
    updated all the endpoints with new db connection
    updated data fecthing from psycopg2 to sqlalchemy query
    created schemas.py to hold request and response model schemas for data.

## 01012022

    @12:20AM
    Created users orm model in models.py
    Added function for create user endpoint
    Added utils.py to store password hashing codes

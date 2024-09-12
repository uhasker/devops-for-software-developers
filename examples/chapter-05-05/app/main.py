from fastapi import FastAPI, HTTPException
from psycopg2 import OperationalError, connect
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "dbname=example user=postgres password=postgres host=exampledb"

class ResponseModel(BaseModel):
    message: str
    db_version: str = None
    error: str = None

@app.get("/", response_model=ResponseModel)
async def root():
    conn = None
    try:
        conn = connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        db_version = cursor.fetchone()[0]
        cursor.close()
        return {"message": "Hello from FastAPI!", "db_version": db_version}
    except OperationalError as e:
        raise HTTPException(status_code=500, detail={"error": "Cannot connect to database", "message": str(e)})
    finally:
        if conn:
            conn.close()

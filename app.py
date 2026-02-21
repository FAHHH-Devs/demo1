import os, time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

DB_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

# --- AUTO-CREATE LOGIC ---
def ensure_table_exists():
    for i in range(10): # Retry loop for slow DB startup
        try:
            with engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS entries (
                        id INT NOT NULL AUTO_INCREMENT,
                        task VARCHAR(255) NOT NULL,
                        done BOOLEAN NOT NULL DEFAULT 0,
                        PRIMARY KEY (id)
                    );
                """))
                conn.commit()
                print("Table 'entries' is ready!")
                return
        except Exception as e:
            print(f"Waiting for database... {e}")
            time.sleep(3)

ensure_table_exists()

class Todo(BaseModel):
    task: str

@app.get("/items")
def get_items():
    with engine.connect() as conn:
        # Use .mappings() to ensure rows are converted to dicts correctly
        result = conn.execute(text("SELECT id, task, done FROM entries"))
        items = [dict(row) for row in result.mappings()] 
        return {"items": items}

@app.post("/items")
def add_item(todo: Todo):
    with engine.connect() as conn:
        # Updated table name to 'entries'
        conn.execute(text("INSERT INTO entries (task) VALUES (:task)"), {"task": todo.task})
        conn.commit()
    return {"status": "success"}

@app.get("/")
def serve_home():
    return FileResponse('static/index.html')
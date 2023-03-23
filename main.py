from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import Database
import schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/connect/")
def connect_to_db(info: schemas.DatabaseConnect, db: Database = Depends(get_db)):

    print(f"Connecting to database {info.name}")

    conn = db.create_connection(
        info.name, info.user, info.password, info.host
    )

    # print("conn: ", conn)

    # db.create_database("test_db_1")

    # conn = db.create_connection(
    #     "test_db_1", "postgres", "postgres", "127.0.0.1"
    # )

    # print("conn1: ", conn)

    return {"db_connection": "successful"}


@app.post("/databases/")
def create_database(database: schemas.DatabaseCreate, db: Database = Depends(get_db)):
    print(f"Creating database {database.name}")
    # if db.connection is None:
    #     db.create_connection()

    db.create_database(database.name)

    return {"db_creation": "successful"}


@app.post("/databases/{database_name}/tables/")
def create_table(database_name: str, table: schemas.TableCreate, db: Database = Depends(get_db)):
    conn = db.create_connection(
        f"{database_name}", "postgres", "postgres", "127.0.0.1"
    )
    db.create_table(table)


@app.get("/databases/{database_name}/tables/{table_name}/columns/")
def get_column_names(database_name: str, table_name: str, db: Database = Depends(get_db)):
    conn = db.create_connection(
        f"{database_name}", "postgres", "postgres", "127.0.0.1"
    )
    results = db.get_column_names(table_name)
    print(results)
    return {"column_names": [result[0] for result in results]}


@app.get("/databases/{database_name}/tables/{table_name}/rows/")
def get_rows(database_name: str, table_name: str, limit: str | None = None, db: Database = Depends(get_db)):
    conn = db.create_connection(
        f"{database_name}", "postgres", "postgres", "127.0.0.1"
    )
    lim = 10
    if limit is not None:
        lim = int(limit)

    results = db.get_rows(table_name, limit=lim)
    print('results: ', results)
    return {"rows": results}
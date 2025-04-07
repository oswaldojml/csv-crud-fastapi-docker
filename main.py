from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import csv
import os
from typing import List


app = FastAPI()
CSV_DIR = "data"
CSV_FILE = CSV_DIR + "/data.csv"


# Initialize CSV
def initialize_csv():
    """Creates CSV if it doesn't exist"""
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nome", "cognome", "codice_fiscale"])

initialize_csv()


# Data model
class Item(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str


#################### Helpers ####################

# Read all records from CSV
def read_csv():
    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

# Write all records to CSV
def write_csv(data: List[dict]):
    with open(CSV_FILE, mode="w", newline="") as file:
        fieldnames = ["id", "nome", "cognome", "codice_fiscale"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


#################### CRUD methods ####################

# Create a new record
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    data = read_csv()
    if any(int(row["id"]) == item.id for row in data):
        raise HTTPException(status_code=400, detail="ID already exists")
    data.append(item.model_dump())
    write_csv(data)
    return item


# Get all records
@app.get("/items/")
def get_items():
    return read_csv()

# Get the number of records
@app.get("/items/count")
def count_items():
    return {"count": len(read_csv())}

# Get a record by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    data = read_csv()
    for row in data:
        if int(row["id"]) == item_id:
            return row
    raise HTTPException(status_code=404, detail="Item not found")


# Update a record by ID
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    data = read_csv()
    for i, row in enumerate(data):
        if int(row["id"]) == item_id:
            data[i] = item.dict()
            write_csv(data)
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# Delete a record by ID
# @app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)# Obs: we shouldn't back information     
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    data = read_csv()
    new_data = [row for row in data if int(row["id"]) != item_id]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Item not found")
    write_csv(new_data)
    return {"message": "Item deleted successfully"}

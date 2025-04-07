# CSV CRUD API with FastAPI and Docker

A simple RESTful API built with **FastAPI** that performs **CRUD operations on a CSV file**. The project is containerized with **Docker**.

## Features

- Create, Read, Update, Delete (CRUD) records in a CSV file
- Each record contains: `id`, `nome`, `cognome`, `codice_fiscale`
- Fully Dockerized

---

## Requirements

- Python 3.13.2
- Docker (for containerized usage)

---

## Run without Docker

```bash
uvicorn main:app --reload
```

## Run with Docker

- Build the image
    ```sh
    docker build -t csv-crud-fastapi .
    ```
- Run the container
    ```sh
    docker run -p 8000:8000 csv-crud-fastapi
    ```
- Alternative: run with volume
    ```sh
    docker run -p 8000:8000 -v ./data:/code/data csv-crud-fastapi
    ```

---

## API Endpoints

| Method | Endpoint         | Description         |
|--------|------------------|---------------------|
| POST   | `/items/`        | Create a new item   |
| GET    | `/items/`        | Get all items       |
| GET    | `/items/{id}`    | Get item by ID      |
| PUT    | `/items/{id}`    | Update item by ID   |
| DELETE | `/items/{id}`    | Delete item by ID   |
| GET    | `/items/count`   | Get total row count |
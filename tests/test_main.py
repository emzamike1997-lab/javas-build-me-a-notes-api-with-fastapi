### === test_notes_api.py ===
```python
from fastapi.testclient import TestClient
from main import app
from notes.models import Note
from notes.database import SessionLocal, engine
from notes.crud import note_crud
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# Create a test client
client = TestClient(app)

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the database session for testing
app.dependency_overrides[SessionLocal] = override_get_db

# Unit tests for notes API
def test_create_note():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    response = client.post("/notes/", json=note_data)
    assert response.status_code == 201
    assert response.json()["title"] == note_data["title"]
    assert response.json()["content"] == note_data["content"]

def test_get_all_notes():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    client.post("/notes/", json=note_data)
    response = client.get("/notes/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_note_by_id():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    response = client.post("/notes/", json=note_data)
    note_id = response.json()["id"]
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id

def test_update_note():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    response = client.post("/notes/", json=note_data)
    note_id = response.json()["id"]
    updated_note_data = {"title": "Updated Test Note", "content": "This is an updated test note"}
    response = client.put(f"/notes/{note_id}", json=updated_note_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_note_data["title"]
    assert response.json()["content"] == updated_note_data["content"]

def test_delete_note():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    response = client.post("/notes/", json=note_data)
    note_id = response.json()["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404

# Integration tests for notes API
def test_create_note_with_invalid_data():
    note_data = {"title": "Test Note"}
    response = client.post("/notes/", json=note_data)
    assert response.status_code == 422

def test_get_note_by_invalid_id():
    response = client.get("/notes/12345")
    assert response.status_code == 404

def test_update_note_with_invalid_data():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    response = client.post("/notes/", json=note_data)
    note_id = response.json()["id"]
    updated_note_data = {"title": "Updated Test Note"}
    response = client.put(f"/notes/{note_id}", json=updated_note_data)
    assert response.status_code == 422

def test_delete_note_with_invalid_id():
    response = client.delete("/notes/12345")
    assert response.status_code == 404

# Test database CRUD operations
def test_create_note_in_database():
    db = TestingSessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    assert note.title == note_data["title"]
    assert note.content == note_data["content"]

def test_get_all_notes_from_database():
    db = TestingSessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note_crud.create_note(db, note_data)
    notes = note_crud.get_all_notes(db)
    assert len(notes) > 0

def test_get_note_by_id_from_database():
    db = TestingSessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note.title == note_data["title"]
    assert retrieved_note.content == note_data["content"]

def test_update_note_in_database():
    db = TestingSessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    updated_note_data = {"title": "Updated Test Note", "content": "This is an updated test note"}
    note_crud.update_note(db, note.id, updated_note_data)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note.title == updated_note_data["title"]
    assert retrieved_note.content == updated_note_data["content"]

def test_delete_note_from_database():
    db = TestingSessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    note_crud.delete_note(db, note.id)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note is None
```

### === test_models.py ===
```python
from notes.models import Note
import pytest

def test_note_model():
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = Note(**note_data)
    assert note.title == note_data["title"]
    assert note.content == note_data["content"]

def test_note_model_with_invalid_data():
    note_data = {"title": "Test Note"}
    with pytest.raises(TypeError):
        Note(**note_data)
```

### === test_database.py ===
```python
from notes.database import SessionLocal, engine
from notes.models import Note
from notes.crud import note_crud
import pytest

def test_database_connection():
    db = SessionLocal()
    assert db is not None

def test_create_note_in_database():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    assert note.title == note_data["title"]
    assert note.content == note_data["content"]

def test_get_all_notes_from_database():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note_crud.create_note(db, note_data)
    notes = note_crud.get_all_notes(db)
    assert len(notes) > 0

def test_get_note_by_id_from_database():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note.title == note_data["title"]
    assert retrieved_note.content == note_data["content"]

def test_update_note_in_database():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    updated_note_data = {"title": "Updated Test Note", "content": "This is an updated test note"}
    note_crud.update_note(db, note.id, updated_note_data)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note.title == updated_note_data["title"]
    assert retrieved_note.content == updated_note_data["content"]

def test_delete_note_from_database():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    note_crud.delete_note(db, note.id)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note is None
```

### === test_crud.py ===
```python
from notes.crud import note_crud
from notes.models import Note
from notes.database import SessionLocal
import pytest

def test_create_note():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    assert note.title == note_data["title"]
    assert note.content == note_data["content"]

def test_get_all_notes():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note_crud.create_note(db, note_data)
    notes = note_crud.get_all_notes(db)
    assert len(notes) > 0

def test_get_note_by_id():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note.title == note_data["title"]
    assert retrieved_note.content == note_data["content"]

def test_update_note():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    updated_note_data = {"title": "Updated Test Note", "content": "This is an updated test note"}
    note_crud.update_note(db, note.id, updated_note_data)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note.title == updated_note_data["title"]
    assert retrieved_note.content == updated_note_data["content"]

def test_delete_note():
    db = SessionLocal()
    note_data = {"title": "Test Note", "content": "This is a test note"}
    note = note_crud.create_note(db, note_data)
    note_crud.delete_note(db, note.id)
    retrieved_note = note_crud.get_note_by_id(db, note.id)
    assert retrieved_note is None
```
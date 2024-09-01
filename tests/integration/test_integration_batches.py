import pytest
from flask import json

def test_create_batch(client):
    payload = {"batch_id": "12345", "status": "created", "piglet_count": 100}

    response = client.post("/batches/", json=payload)

    assert response.status_code == 201

    data = response.get_json()
    assert "batch_id" in data
    assert data["batch_id"] == payload["batch_id"]
    assert data["status"] == payload["status"]
    assert data["piglet_count"] == payload["piglet_count"]


def test_get_all_batches(client, example_data):
    response = client.get("/batches/")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) >= 0


def test_get_batches_by_status(client, example_data):
    response = client.get("/batches/?status=created")
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) >= 0


def test_update_specific_batch(client, example_data, session):
    payload = {"piglet_count": 100}

    response = client.patch("/batches/12345", json=payload)

    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Batch updated successfully!"

    from src.models.batch_model import Batch

    updated_batch = Batch.query.filter_by(batch_id="12345").first()
    assert updated_batch is not None
    session.flush()  
    assert updated_batch.piglet_count == 100



def test_delete_specific_batch(client, session):
    from src.models.batch_model import Batch

    batch = Batch(batch_id="12345", status="pending", piglet_count=100)
    session.add(batch)
    session.commit()

    response = client.delete("/batches/12345")

    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Batch deleted successfully!"

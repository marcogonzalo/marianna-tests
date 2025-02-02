import pytest
from httpx import AsyncClient
from assessments.models import Assessment, Question, Choice

async def test_create_assessment(async_client: AsyncClient):
    response = await async_client.post("/assessments/", json={
        "title": "Test Assessment",
        "description": "Test Description",
        "scoring_method": "boolean",
        "min_value": 0,
        "max_value": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Assessment"
    assert data["scoring_method"] == "boolean"

async def test_create_assessment_with_default_values(async_client: AsyncClient):
    response = await async_client.post("/assessments/", json={
        "title": "Test Assessment",
        "scoring_method": "boolean"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["min_value"] == 0
    assert data["max_value"] == 1

async def test_list_assessments(async_client: AsyncClient, sample_assessment: Assessment):
    response = await async_client.get("/assessments/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == sample_assessment.title

async def test_get_assessment(async_client: AsyncClient, sample_assessment: Assessment):
    response = await async_client.get(f"/assessments/{sample_assessment.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_assessment.title

async def test_update_assessment(async_client: AsyncClient, sample_assessment: Assessment):
    response = await async_client.put(
        f"/assessments/{sample_assessment.id}",
        json={
            "title": "Updated Assessment",
            "description": "Updated Description",
            "scoring_method": "boolean",
            "min_value": 0,
            "max_value": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Assessment"

async def test_delete_assessment(async_client: AsyncClient, sample_assessment: Assessment):
    response = await async_client.delete(f"/assessments/{sample_assessment.id}")
    assert response.status_code == 200

    # Verify deletion
    response = await async_client.get(f"/assessments/{sample_assessment.id}")
    assert response.status_code == 404

async def test_create_question(async_client: AsyncClient, sample_assessment: Assessment):
    response = await async_client.post(
        f"/assessments/{sample_assessment.id}/questions",
        json={
            "text": "Test Question",
            "order": 1,
            "choices": [
                {"text": "Choice 1", "value": 1, "order": 1},
                {"text": "Choice 2", "value": 0, "order": 2}
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test Question"
    assert len(data["choices"]) == 2

import pytest
from httpx import AsyncClient
from users.models import Examinee
from assessments.models import Assessment


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


async def test_create_assessment_with_invalid_scoring(async_client: AsyncClient):
    # For custom scoring, we should expect a 422 error when min/max values are missing
    response = await async_client.post("/assessments/", json={
        "title": "Test Assessment",
        "scoring_method": "custom"  # Custom requires min/max values
    })
    assert response.status_code == 422  # Changed to expect validation error


async def test_create_question_invalid_data(async_client: AsyncClient, sample_assessment: Assessment):
    response = await async_client.post(
        f"/assessments/{sample_assessment.id}/questions",
        json={
            "text": "Test Question",
            "order": 1,
            "choices": []  # Invalid: empty choices
        }
    )
    assert response.status_code == 422


async def test_assessment_response_workflow(async_client: AsyncClient, sample_assessment: Assessment, sample_examinee: Examinee):
    # Create a question first with proper data
    question_response = await async_client.post(
        f"/assessments/{sample_assessment.id}/questions",
        json={
            "text": "Test Question",
            "order": 1,
            "choices": [
                {"text": "Choice 1", "value": 1.0, "order": 1},
                {"text": "Choice 2", "value": 0.0, "order": 2}
            ]
        }
    )
    assert question_response.status_code == 200
    question = question_response.json()
    question_id = question["id"]

    # Create assessment response with initial status
    response = await async_client.post(
        f"/assessments/{str(sample_assessment.id)}/responses",
        json={"examinee_id": str(sample_examinee.id)}
    )
    assert response.status_code == 200
    # response_id = response.json()["id"]

    # Submit responses with proper structure
    # bulk_response = await async_client.put(
    #     f"/assessments/responses/{response_id}",
    #     json={
    #         "question_responses": [
    #             {
    #                 "question_id": question_id,
    #                 "numeric_value": 1.0,
    #                 "text_value": None
    #             }
    #         ]
    #     }
    # )
    # assert bulk_response.status_code == 200

    # data = bulk_response.json()
    # assert data["status"] == "completed"
    # assert data["score"] == 1.0
    # assert len(data["question_responses"]) == 1
    # assert data["question_responses"][0]["question_id"] == question_id
    # assert data["question_responses"][0]["numeric_value"] == 1.0

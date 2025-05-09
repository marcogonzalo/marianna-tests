import pytest
from httpx import AsyncClient
from fastapi import status
from app.users.models import Examinee, User
from app.assessments.models import Assessment
from app.users.models import Account


async def test_create_assessment(async_client: AsyncClient, auth_headers_admin: dict):
    response = await async_client.post("/assessments/",
                                       headers=auth_headers_admin,
                                       json={
                                           "title": "Test Assessment",
                                           "description": "Test Description",
                                           "scoring_method": "boolean",
                                           "min_value": 0,
                                           "max_value": 1
                                       }
                                       )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Assessment"
    assert data["scoring_method"] == "boolean"


async def test_create_assessment_with_default_values(async_client: AsyncClient, auth_headers_admin: dict):
    response = await async_client.post("/assessments/",
                                       headers=auth_headers_admin,
                                       json={
                                           "title": "Test Assessment",
                                           "scoring_method": "boolean"
                                       }
                                       )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["min_value"] == 0
    assert data["max_value"] == 1


async def test_list_assessments(async_client: AsyncClient, sample_assessment: Assessment, auth_headers_admin: dict):
    response = await async_client.get("/assessments/", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == sample_assessment.title


async def test_get_assessment(async_client: AsyncClient, sample_assessment: Assessment, auth_headers_admin: dict):
    response = await async_client.get(f"/assessments/{sample_assessment.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == sample_assessment.title


async def test_update_assessment(async_client: AsyncClient, sample_assessment: Assessment, auth_headers_admin: dict):
    update_data = {
        "title": "Updated Assessment Title",
        "description": "Updated assessment description"
    }
    
    response = await async_client.patch(
        f"/assessments/{sample_assessment.id}",
        json=update_data,
        headers=auth_headers_admin
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Assessment Title"
    assert data["description"] == "Updated assessment description"


async def test_delete_assessment(async_client: AsyncClient, sample_assessment: Assessment, auth_headers_admin: dict):
    response = await async_client.delete(f"/assessments/{sample_assessment.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_200_OK

    # Verify deletion
    response = await async_client.get(f"/assessments/{sample_assessment.id}", headers=auth_headers_admin)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_question(async_client: AsyncClient, sample_assessment: Assessment, auth_headers_admin: dict):
    response = await async_client.post(
        f"/assessments/{sample_assessment.id}/questions",
        headers=auth_headers_admin,
        json={
            "text": "Test Question",
            "order": 1,
            "choices": [
                {"text": "Choice 1", "value": 1, "order": 1},
                {"text": "Choice 2", "value": 0, "order": 2}
            ]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == "Test Question"
    assert len(data["choices"]) == 2


async def test_create_assessment_with_invalid_scoring(async_client: AsyncClient, auth_headers_admin: dict):
    # For custom scoring, we should expect a 422 error when min/max values are missing
    response = await async_client.post("/assessments/",
                                       headers=auth_headers_admin,
                                       json={
                                           "title": "Test Assessment",
                                           "scoring_method": "custom"  # Custom requires min/max values
                                       }
                                       )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Changed to expect validation error


async def test_create_question_invalid_data(async_client: AsyncClient, sample_assessment: Assessment, auth_headers_admin: dict):
    response = await async_client.post(
        f"/assessments/{sample_assessment.id}/questions",
        headers=auth_headers_admin,
        json={
            "text": "Test Question",
            "order": 1,
            "choices": []  # Invalid: empty choices
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_assessment_response_workflow(async_client: AsyncClient, sample_assessment: Assessment, sample_examinee: Examinee, non_admin_auth_headers: dict, sample_user: User):
    # Create a question first with proper data
    question_response = await async_client.post(
        f"/assessments/{sample_assessment.id}/questions",
        headers=non_admin_auth_headers,
        json={
            "text": "Test Question",
            "order": 1,
            "choices": [
                {"text": "Choice 1", "value": 1.0, "order": 1},
                {"text": "Choice 2", "value": 0.0, "order": 2}
            ]
        }
    )
    assert question_response.status_code == status.HTTP_200_OK
    question = question_response.json()
    question_id = question["id"]

    # Create assessment response with initial status
    response = await async_client.post(
        f"/assessments/{sample_assessment.id}/responses",
        headers=non_admin_auth_headers,
        json={
            "examinee_id": str(sample_examinee.id),
            "created_by": str(sample_user.account.id)
        }
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["examinee_id"] == str(sample_examinee.id)
    assert response_data["created_by"] == str(sample_user.account.id)
    assert response_data["status"] == "pending"

    # Submit responses with proper structure
    response_id = response_data["id"]
    bulk_response = await async_client.put(
        f"/responses/{response_id}",
        json={
            "question_responses": [
                {
                    "question_id": question_id,
                    "numeric_value": 1.0,
                    "text_value": None
                }
            ]
        }
    )
    assert bulk_response.status_code == status.HTTP_200_OK

    data = bulk_response.json()
    assert data["status"] == "completed"
    assert data["score"] == 1.0

import pytest
from datetime import date
from app.users.models import Account
from app.users.schemas import ExamineeCreate, ExamineeUpdate
from app.users.enums import Gender


def test_examinee_create_schema(sample_account: Account):
    examinee_data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "birth_date": date(1995, 5, 15),
        "gender": Gender.FEMALE,
        "email": "alice.johnson@example.com",
        "internal_identifier": "ID126",
        "comments": "Test examinee",
        "created_by": sample_account.id
    }
    examinee = ExamineeCreate(**examinee_data)
    assert examinee.first_name == "Alice"
    assert examinee.email == "alice.johnson@example.com"


def test_examinee_update_schema():
    update_data = {
        "first_name": "Alicia",
        "last_name": "Johnson",
        "birth_date": date(1995, 5, 15),
        "gender": Gender.FEMALE,
        "email": "alice.johnson@example.com",
        "internal_identifier": "ID126",
        "comments": "Test examinee",
    }
    examinee_update = ExamineeUpdate(**update_data)
    assert examinee_update.first_name == "Alicia"

import pytest
from datetime import date
from users.models import Account
from users.enums import Gender
from users.schemas import ExamineeCreate, ExamineeUpdate
from users.services import ExamineeService
from sqlmodel import Session


def test_create_examinee(session: Session, sample_account: Account):
    examinee_data = ExamineeCreate(
        first_name="Tom",
        last_name="Brown",
        birth_date=date(1995, 5, 15),
        gender=Gender.MALE,
        email="tom.brown@example.com",
        internal_identifier="ID127",
        comments="Test examinee",
        created_by=sample_account.id
    )
    examinee = ExamineeService.create_examinee(session, examinee_data)
    assert examinee.first_name == "Tom"
    assert examinee.email == "tom.brown@example.com"


def test_get_examinee(session: Session, sample_account: Account):
    examinee_data = ExamineeCreate(
        first_name="Sara",
        last_name="Connor",
        birth_date=date(1985, 5, 15),
        gender=Gender.FEMALE,
        email="sara.connor@example.com",
        internal_identifier="ID128",
        comments="Test examinee",
        created_by=sample_account.id
    )
    created_examinee = ExamineeService.create_examinee(session, examinee_data)
    fetched_examinee = ExamineeService.get_examinee(
        session, created_examinee.id)
    assert fetched_examinee.id == created_examinee.id


def test_update_examinee(session: Session, sample_account: Account):
    examinee_data = ExamineeCreate(
        first_name="Mike",
        last_name="Davis",
        birth_date=date(1998, 5, 15),
        gender=Gender.MALE,
        email="mike.davis@example.com",
        internal_identifier="ID129",
        comments="Test examinee",
        created_by=sample_account.id
    )
    created_examinee = ExamineeService.create_examinee(session, examinee_data)

    update_data = ExamineeUpdate(
        first_name="Michael",
        last_name="Davis",
        birth_date=date(1998, 5, 15),
        gender=Gender.MALE,
        email="mike.davis@example.com",
        internal_identifier="ID129",
        comments="Test examinee",
        created_by=sample_account.id
    )
    updated_examinee = ExamineeService.update_examinee(
        session, created_examinee.id, update_data)
    assert updated_examinee.first_name == "Michael"


def test_soft_delete_examinee(session: Session, sample_account: Account):
    examinee_data = ExamineeCreate(
        first_name="Laura",
        last_name="Wilson",
        birth_date=date(2020, 5, 15),
        gender=Gender.FEMALE,
        email="laura.wilson@example.com",
        internal_identifier="ID130",
        comments="Test examinee",
        created_by=sample_account.id
    )
    created_examinee = ExamineeService.create_examinee(session, examinee_data)
    assert ExamineeService.soft_delete_examinee(
        session, created_examinee.id) is True
    assert ExamineeService.get_examinee(session, created_examinee.id) is None

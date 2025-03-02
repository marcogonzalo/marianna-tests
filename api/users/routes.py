from fastapi import APIRouter, Depends, HTTPException
from httpx import request
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List
from database import get_session
from auth.decorators import requires_auth
from .schemas import UserAccountCreate, UserRead, UserUpdate, AccountCreate, AccountRead, AccountUpdate
from .services import UserService, AccountService
from .schemas import ExamineeCreate, ExamineeRead, ExamineeUpdate
from .services import ExamineeService

users_router = APIRouter(prefix="/users", tags=["users"])
accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])
examinees_router = APIRouter(prefix="/examinees", tags=["examinees"])


@users_router.post("/", response_model=UserRead)
@requires_auth
def create_user(user: UserAccountCreate, session: Session = Depends(get_session), token=None):
    db_user = UserService.get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user_account(session=session, user=user)


@users_router.get("/", response_model=List[UserRead])
@requires_auth
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session), token=None):
    users = UserService.get_users(session, skip=skip, limit=limit)
    return users


@users_router.get("/{id}", response_model=UserRead)
@requires_auth
def read_user(id: UUID4, session: Session = Depends(get_session), token=None):
    db_user = UserService.get_user(session, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.put("/{id}", response_model=UserRead)
@requires_auth
def update_user(id: UUID4, user: UserUpdate, session: Session = Depends(get_session), token=None):
    db_user = UserService.update_user(session, id=id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.delete("/{id}")
@requires_auth
def delete_user(id: UUID4, session: Session = Depends(get_session), token=None):
    success = UserService.delete_user(session, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


# @users_router.post("/{id}/restore")
# def restore_user(id: UUID4, session: Session = Depends(get_session)):
#     success = UserService.restore_user(session, id=id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found or not deleted")
#     return {"detail": "User restored"}


@accounts_router.post("/", response_model=AccountRead)
@requires_auth
def create_account(account: AccountCreate, user_id: UUID4, session: Session = Depends(get_session), token=None):
    return AccountService.create_account(session=session, account=account, user_id=user_id)


@accounts_router.get("/", response_model=List[AccountRead])
@requires_auth
def read_accounts(skip: int = 0, limit: int = 100, session: Session = Depends(get_session), token=None):
    accounts = AccountService.get_accounts(session, skip=skip, limit=limit)
    return accounts


@accounts_router.get("/{id}", response_model=AccountRead)
@requires_auth
def read_account(id: UUID4, session: Session = Depends(get_session), token=None):
    db_account = AccountService.get_account(session, id=id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@accounts_router.put("/{id}", response_model=AccountRead)
@requires_auth
def update_account(id: UUID4, account: AccountUpdate, session: Session = Depends(get_session), token=None):
    db_account = AccountService.update_account(session, id=id, account=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@accounts_router.delete("/{id}")
@requires_auth
def delete_account(id: UUID4, session: Session = Depends(get_session), token=None):
    success = AccountService.delete_account(session, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted"}


@examinees_router.post("/", response_model=ExamineeRead)
@requires_auth
def create_examinee(examinee: ExamineeCreate, session: Session = Depends(get_session), token=None):
    return ExamineeService.create_examinee(session, examinee)


@examinees_router.get("/{id}", response_model=ExamineeRead)
@requires_auth
def get_examinee(id: UUID4, session: Session = Depends(get_session), token=None):
    examinee = ExamineeService.get_examinee(session, id)
    if not examinee:
        raise HTTPException(status_code=404, detail="Examinee not found")
    return examinee


@examinees_router.get("/", response_model=list[ExamineeRead])
@requires_auth
def get_examinees(skip: int = 0, limit: int = 100, session: Session = Depends(get_session), token=None):
    return ExamineeService.get_examinees(session, skip, limit)


@examinees_router.put("/{id}", response_model=ExamineeRead)
@requires_auth
def update_examinee(id: UUID4, examinee: ExamineeUpdate, session: Session = Depends(get_session), token=None):
    updated_examinee = ExamineeService.update_examinee(session, id, examinee)
    if not updated_examinee:
        raise HTTPException(status_code=404, detail="Examinee not found")
    return updated_examinee


@examinees_router.delete("/{id}", response_model=dict)
@requires_auth
def soft_delete_examinee(id: UUID4, session: Session = Depends(get_session), token=None):
    if request.query_params.get("hard_delete"):
        success = ExamineeService.hard_delete_examinee(session, id)
    else:
        success = ExamineeService.soft_delete_examinee(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Examinee not found")
    return {"detail": "Examinee deleted"}

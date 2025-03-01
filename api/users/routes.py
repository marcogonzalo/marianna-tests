from fastapi import APIRouter, Depends, HTTPException, status
from httpx import request
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List
from database import get_session
from auth.routes import get_current_user
from .models import User
from .schemas import UserAccountCreate, UserRead, UserUpdate, AccountCreate, AccountRead, AccountUpdate
from .services import UserService, AccountService
from .schemas import ExamineeCreate, ExamineeRead, ExamineeUpdate
from .services import ExamineeService

users_router = APIRouter(prefix="/users", tags=["users"])
accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])
examinees_router = APIRouter(prefix="/examinees", tags=["examinees"])


@users_router.post("/", response_model=UserRead)
def create_user(user: UserAccountCreate, db: Session = Depends(get_session)):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user_account(db=db, user=user)


@users_router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/{id}", response_model=UserRead)
def read_user(id: UUID4, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_user = UserService.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.put("/{id}", response_model=UserRead)
def update_user(id: UUID4, user: UserUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_user = UserService.update_user(db, id=id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.delete("/{id}")
def delete_user(id: UUID4, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success = UserService.delete_user(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


# @users_router.post("/{id}/restore")
# def restore_user(id: UUID4, db: Session = Depends(get_session)):
#     success = UserService.restore_user(db, id=id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found or not deleted")
#     return {"detail": "User restored"}


@accounts_router.post("/", response_model=AccountRead)
def create_account(account: AccountCreate, user_id: UUID4, db: Session = Depends(get_session)):
    return AccountService.create_account(db=db, account=account, user_id=user_id)


@accounts_router.get("/", response_model=List[AccountRead])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    accounts = AccountService.get_accounts(db, skip=skip, limit=limit)
    return accounts


@accounts_router.get("/{id}", response_model=AccountRead)
def read_account(id: UUID4, db: Session = Depends(get_session)):
    db_account = AccountService.get_account(db, id=id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@accounts_router.put("/{id}", response_model=AccountRead)
def update_account(id: UUID4, account: AccountUpdate, db: Session = Depends(get_session)):
    db_account = AccountService.update_account(db, id=id, account=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@accounts_router.delete("/{id}")
def delete_account(id: UUID4, db: Session = Depends(get_session)):
    success = AccountService.delete_account(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted"}


@examinees_router.post("/", response_model=ExamineeRead)
def create_examinee(examinee: ExamineeCreate, db: Session = Depends(get_session)):
    return ExamineeService.create_examinee(db, examinee)


@examinees_router.get("/{id}", response_model=ExamineeRead)
def get_examinee(id: UUID4, db: Session = Depends(get_session)):
    examinee = ExamineeService.get_examinee(db, id)
    if not examinee:
        raise HTTPException(status_code=404, detail="Examinee not found")
    return examinee


@examinees_router.get("/", response_model=list[ExamineeRead])
def get_examinees(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return ExamineeService.get_examinees(db, skip, limit)


@examinees_router.put("/{id}", response_model=ExamineeRead)
def update_examinee(id: UUID4, examinee: ExamineeUpdate, db: Session = Depends(get_session)):
    updated_examinee = ExamineeService.update_examinee(db, id, examinee)
    if not updated_examinee:
        raise HTTPException(status_code=404, detail="Examinee not found")
    return updated_examinee


@examinees_router.delete("/{id}", response_model=dict)
def soft_delete_examinee(id: UUID4, db: Session = Depends(get_session)):
    if request.query_params.get("hard_delete"):
        success = ExamineeService.hard_delete_examinee(db, id)
    else:
        success = ExamineeService.soft_delete_examinee(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Examinee not found")
    return {"detail": "Examinee deleted"}

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List
from database import get_session
from .schemas import UserCreate, UserRead, UserUpdate, AccountCreate, AccountRead, AccountUpdate
from .services import UserService, AccountService

users_router = APIRouter(prefix="/users", tags=["users"])
accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])


@users_router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user)


@users_router.get("/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/{id}", response_model=UserRead)
def read_user(id: UUID4, db: Session = Depends(get_session)):
    db_user = UserService.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.put("/{id}", response_model=UserRead)
def update_user(id: UUID4, user: UserUpdate, db: Session = Depends(get_session)):
    db_user = UserService.update_user(db, id=id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.delete("/{id}")
def delete_user(id: UUID4, db: Session = Depends(get_session)):
    success = UserService.delete_user(db, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


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

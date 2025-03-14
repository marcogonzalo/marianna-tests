from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import UUID4
from sqlalchemy.orm import Session
from typing import List
from app.users.enums import UserRole, all_user_roles
from database import get_session
from app.auth.services import AuthService, RoleChecker
from .schemas import UserAccountCreate, UserRead, UserUpdate, AccountCreate, AccountRead, AccountUpdate
from .schemas import ExamineeCreate, ExamineeRead, ExamineeUpdate
from .services import UserService, AccountService, ExamineeService

users_router = APIRouter(prefix="/users", tags=["users"])
accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])
examinees_router = APIRouter(prefix="/examinees", tags=["examinees"])


@users_router.post("/", response_model=UserRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def create_user(user: UserAccountCreate, session: Session = Depends(get_session)):
    db_user = UserService.get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return UserService.create_user_account(session=session, user=user)


@users_router.get("/", response_model=List[UserRead], dependencies=[Depends(RoleChecker(all_user_roles))])
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = UserService.get_users(session, skip=skip, limit=limit)
    return users


@users_router.get("/me", response_model=UserRead, dependencies=[Depends(RoleChecker(all_user_roles))])
def read_current_user(current_user=Depends(AuthService.get_current_active_user)):
    return current_user


@users_router.get("/{id}", response_model=UserRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def read_user(id: UUID4, session: Session = Depends(get_session)):
    db_user = UserService.get_user(session, id=id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@users_router.put("/{id}", response_model=UserRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def update_user(id: UUID4, user: UserUpdate, session: Session = Depends(get_session)):
    db_user = UserService.update_user(session, id=id, user=user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@users_router.delete("/{id}", dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def delete_user(id: UUID4, session: Session = Depends(get_session)):
    success = UserService.delete_user(session, id=id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "User deleted"}


# @users_router.post("/{id}/restore")
# def restore_user(id: UUID4, session: Session = Depends(get_session)):
#     success = UserService.restore_user(session, id=id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found or not deleted")
#     return {"detail": "User restored"}


@accounts_router.post("/", response_model=AccountRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def create_account(account: AccountCreate, user_id: UUID4, session: Session = Depends(get_session)):
    return AccountService.create_account(session=session, account=account, user_id=user_id)


@accounts_router.get("/", response_model=List[AccountRead], dependencies=[Depends(RoleChecker(all_user_roles))])
def read_accounts(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    accounts = AccountService.get_accounts(session, skip=skip, limit=limit)
    return accounts


@accounts_router.get("/{id}", response_model=AccountRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def read_account(id: UUID4, session: Session = Depends(get_session)):
    db_account = AccountService.get_account(session, id=id)
    if db_account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return db_account


@accounts_router.put("/{id}", response_model=AccountRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def update_account(id: UUID4, account: AccountUpdate, session: Session = Depends(get_session)):
    db_account = AccountService.update_account(session, id=id, account=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@accounts_router.delete("/{id}", dependencies=[Depends(RoleChecker([UserRole.ADMIN]))])
def delete_account(id: UUID4, session: Session = Depends(get_session)):
    success = AccountService.delete_account(session, id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted"}


@examinees_router.post("/", response_model=ExamineeRead, dependencies=[Depends(RoleChecker(all_user_roles))])
def create_examinee(examinee: ExamineeCreate, session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)):
    examinee.created_by = current_user.account.id
    return ExamineeService.create_examinee(session, examinee)


@examinees_router.get("/", response_model=list[ExamineeRead], dependencies=[Depends(RoleChecker(all_user_roles))])
def get_examinees(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return ExamineeService.get_examinees(session, skip, limit)


@examinees_router.get("/{id}", response_model=ExamineeRead, dependencies=[Depends(RoleChecker(all_user_roles))])
def get_examinee(id: UUID4, session: Session = Depends(get_session)):
    examinee = ExamineeService.get_examinee(session, id)
    if not examinee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Examinee not found")
    return examinee


@examinees_router.put("/{id}", response_model=ExamineeRead, dependencies=[Depends(RoleChecker(all_user_roles))])
def update_examinee(id: UUID4, examinee: ExamineeUpdate, session: Session = Depends(get_session)):
    updated_examinee = ExamineeService.update_examinee(session, id, examinee)
    if not updated_examinee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Examinee not found")
    return updated_examinee


@examinees_router.delete("/{id}", response_model=dict, dependencies=[Depends(RoleChecker(all_user_roles))])
def soft_delete_examinee(
    id: UUID4,
    request: Request,
    session: Session = Depends(get_session),
    current_user=Depends(AuthService.get_current_active_user)
):
    hard_delete = request.query_params.get("hard_delete") == "true"
    if hard_delete:
        if current_user.account.role != UserRole.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: Only admins can perform a hard delete")
        success = ExamineeService.hard_delete_examinee(session, id)
    else:
        success = ExamineeService.soft_delete_examinee(session, id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Examinee not found")
    return {"detail": "Examinee deleted"}

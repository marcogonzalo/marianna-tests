from datetime import datetime, timezone
from typing import List, Optional
from pydantic import UUID4
from sqlalchemy.orm import Session, joinedload
from .models import User, Account
from .schemas import UserAccountCreate, UserCreate, UserRead, UserUpdate, AccountCreate, AccountRead, AccountUpdate
from utils.password import get_password_hash


class UserService:
    @staticmethod
    def get_user(db: Session, id: str) -> Optional[UserRead]:
        db_user = db.query(User).filter(User.id == id, User.deleted_at.is_(None)).options(
            joinedload(User.account)
        ).first()
        return UserRead.model_validate(db_user) if db_user else None

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[UserRead]:
        db_user = db.query(User).filter(User.email == email, User.deleted_at.is_(None)).options(
            joinedload(User.account)
        ).first()
        return UserRead.model_validate(db_user) if db_user else None

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserRead]:
        db_users = db.query(User).filter(User.deleted_at.is_(None)).options(
            joinedload(User.account)
        ).offset(skip).limit(limit).all()
        return [UserRead.model_validate(user) for user in db_users]

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserRead:
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserRead.model_validate(db_user)

    @staticmethod
    def create_user_account(db: Session, user: UserAccountCreate) -> UserRead:
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        if user.account:
            user_id_uuid = UUID4(db_user.id) if isinstance(
                db_user.id, str) else db_user.id
            db_account = Account(
                **user.account.model_dump(), user_id=user_id_uuid)
            db.add(db_account)
            db.commit()
            db.refresh(db_account)
            db_user.account = db_account
        return UserRead.model_validate(db_user)

    @staticmethod
    def update_user(db: Session, id: str, user: UserUpdate) -> Optional[UserRead]:
        db_user = db.query(User).filter(User.id == id).first()
        if db_user:
            update_data = user.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["password_hash"] = get_password_hash(
                    update_data.pop("password"))
            for key, value in update_data.items():
                setattr(db_user, key, value)
            db_user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_user)
            return UserRead.model_validate(db_user)
        return None

    @staticmethod
    def delete_user(db: Session, id: str) -> bool:
        db_user = db.query(User).filter(
            User.id == id, User.deleted_at.is_(None)).first()
        if db_user:
            db_user.deleted_at = datetime.now(timezone.utc)
            db.commit()
            return True
        return False

    @staticmethod
    def restore_user(db: Session, id: str) -> bool:
        db_user = db.query(User).filter(
            User.id == id,
            User.deleted_at.is_not(None)
        ).first()
        if db_user:
            db_user.deleted_at = None
            db_user.updated_at = datetime.now(timezone.utc)
            db.commit()
            return True
        return False


class AccountService:
    @staticmethod
    def get_account(db: Session, id: str) -> Optional[AccountRead]:
        db_account = db.query(Account).filter(Account.id == id).first()
        return AccountRead.model_validate(db_account) if db_account else None

    @staticmethod
    def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[AccountRead]:
        db_accounts = db.query(Account).offset(skip).limit(limit).all()
        return [AccountRead.model_validate(account) for account in db_accounts]

    @staticmethod
    def create_account(db: Session, account: AccountCreate, user_id: str) -> AccountRead:
        user_id_uuid = UUID4(user_id) if isinstance(user_id, str) else user_id
        db_account = Account(**account.model_dump(), user_id=user_id_uuid)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return AccountRead.model_validate(db_account)

    @staticmethod
    def update_account(db: Session, id: str, account: AccountUpdate) -> Optional[AccountRead]:
        db_account = db.query(Account).filter(Account.id == id).first()
        if db_account:
            update_data = account.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_account, key, value)
            db_account.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_account)
            return AccountRead.model_validate(db_account)
        return None

    @staticmethod
    def delete_account(db: Session, id: str) -> bool:
        db_account = db.query(Account).filter(Account.id == id).first()
        if db_account:
            db.delete(db_account)
            db.commit()
            return True
        return False

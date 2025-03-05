from datetime import datetime, timezone
from typing import List, Optional
from pydantic import UUID4
from sqlalchemy.orm import Session, joinedload
from .models import User, Account, Examinee
from .schemas import UserAccountCreate, UserCreate, UserRead, UserUpdate, AccountCreate, AccountRead, AccountUpdate, ExamineeCreate, ExamineeRead, ExamineeUpdate
from app.utils.password import get_password_hash


class UserService:
    @staticmethod
    def get_user(session: Session, id: str) -> Optional[UserRead]:
        db_user = session.query(User).filter(User.id == id, User.deleted_at.is_(None)).options(
            joinedload(User.account)
        ).first()
        return UserRead.model_validate(db_user) if db_user else None

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        db_user = session.query(User).filter(User.email == email, User.deleted_at.is_(None)).options(
            joinedload(User.account)
        ).first()
        return db_user  # Return the DB model directly instead of converting to UserRead

    @staticmethod
    def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[UserRead]:
        db_users = session.query(User).filter(User.deleted_at.is_(None)).options(
            joinedload(User.account)
        ).offset(skip).limit(limit).all()
        return [UserRead.model_validate(user) for user in db_users]

    @staticmethod
    def create_user(session: Session, user: UserCreate) -> UserRead:
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return UserRead.model_validate(db_user)

    @staticmethod
    def create_user_account(session: Session, user: UserAccountCreate) -> UserRead:
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        if user.account:
            user_id_uuid = UUID4(db_user.id) if isinstance(
                db_user.id, str) else db_user.id
            db_account = Account(
                **user.account.model_dump(), user_id=user_id_uuid)
            session.add(db_account)
            session.commit()
            session.refresh(db_account)
            db_user.account = db_account
        return UserRead.model_validate(db_user)

    @staticmethod
    def update_user(session: Session, id: str, user: UserUpdate) -> Optional[UserRead]:
        db_user = session.query(User).filter(User.id == id).first()
        if db_user:
            update_data = user.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["password_hash"] = get_password_hash(
                    update_data.pop("password"))
            for key, value in update_data.items():
                setattr(db_user, key, value)
            db_user.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(db_user)
            return UserRead.model_validate(db_user)
        return None

    @staticmethod
    def delete_user(session: Session, id: str) -> bool:
        db_user = session.query(User).filter(
            User.id == id, User.deleted_at.is_(None)).first()
        if db_user:
            db_user.deleted_at = datetime.now(timezone.utc)
            session.commit()
            return True
        return False

    @staticmethod
    def restore_user(session: Session, id: str) -> bool:
        db_user = session.query(User).filter(
            User.id == id,
            User.deleted_at.is_not(None)
        ).first()
        if db_user:
            db_user.deleted_at = None
            db_user.updated_at = datetime.now(timezone.utc)
            session.commit()
            return True
        return False


class AccountService:
    @staticmethod
    def get_account(session: Session, id: str) -> Optional[AccountRead]:
        db_account = session.query(Account).filter(Account.id == id).first()
        return AccountRead.model_validate(db_account) if db_account else None

    @staticmethod
    def get_accounts(session: Session, skip: int = 0, limit: int = 100) -> List[AccountRead]:
        db_accounts = session.query(Account).offset(skip).limit(limit).all()
        return [AccountRead.model_validate(account) for account in db_accounts]

    @staticmethod
    def create_account(session: Session, account: AccountCreate, user_id: str) -> AccountRead:
        user_id_uuid = UUID4(user_id) if isinstance(user_id, str) else user_id
        db_account = Account(**account.model_dump(), user_id=user_id_uuid)
        session.add(db_account)
        session.commit()
        session.refresh(db_account)
        return AccountRead.model_validate(db_account)

    @staticmethod
    def update_account(session: Session, id: str, account: AccountUpdate) -> Optional[AccountRead]:
        db_account = session.query(Account).filter(Account.id == id).first()
        if db_account:
            update_data = account.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_account, key, value)
            db_account.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(db_account)
            return AccountRead.model_validate(db_account)
        return None

    @staticmethod
    def delete_account(session: Session, id: str) -> bool:
        db_account = session.query(Account).filter(Account.id == id).first()
        if db_account:
            session.delete(db_account)
            session.commit()
            return True
        return False


class ExamineeService:
    @staticmethod
    def get_examinee(session: Session, id: str) -> Optional[ExamineeRead]:
        db_examinee = session.query(Examinee).filter(
            Examinee.id == id, Examinee.deleted_at.is_(None)).first()
        return ExamineeRead.model_validate(db_examinee.model_dump()) if db_examinee else None

    @staticmethod
    def get_examinees(session: Session, skip: int = 0, limit: int = 100) -> List[ExamineeRead]:
        db_examinees = session.query(Examinee).filter(
            Examinee.deleted_at.is_(None)).offset(skip).limit(limit).all()
        return [ExamineeRead.model_validate(examinee.model_dump()) for examinee in db_examinees]

    @staticmethod
    def create_examinee(session: Session, examinee: ExamineeCreate) -> ExamineeRead:
        db_examinee = Examinee(**examinee.model_dump())
        db_account = session.query(Account).filter(
            Account.id == examinee.created_by).first()
        if db_account:
            db_examinee.created_by = db_account.id
        session.add(db_examinee)
        session.commit()
        session.refresh(db_examinee)
        return ExamineeRead.model_validate(db_examinee.model_dump())

    @staticmethod
    def update_examinee(session: Session, id: str, examinee: ExamineeUpdate) -> Optional[ExamineeRead]:
        db_examinee = session.query(Examinee).filter(Examinee.id == id).first()
        if db_examinee:
            update_data = examinee.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_examinee, key, value)
            db_examinee.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(db_examinee)
            return ExamineeRead.model_validate(db_examinee.model_dump())
        return None

    @staticmethod
    def soft_delete_examinee(session: Session, id: str) -> bool:
        db_examinee = session.query(Examinee).filter(Examinee.id == id).first()
        if db_examinee:
            db_examinee.deleted_at = datetime.now(timezone.utc)
            session.commit()
            return True
        return False

    @staticmethod
    def hard_delete_examinee(session: Session, id: str) -> bool:
        db_examinee = session.query(Examinee).filter(Examinee.id == id).first()
        if db_examinee:
            session.delete(db_examinee)
            session.commit()
            return True
        return False

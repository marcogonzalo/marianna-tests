import os
import sys
from pathlib import Path


# Add the project root directory to Python path
project_root = Path(__file__).parent.parent  # nopep8
sys.path.append(str(project_root))  # nopep8

from sqlmodel import Session, create_engine, select
from app.users.models import User
from app.users.schemas import UserAccountCreate, AccountCreate
from app.users.services import UserService
from getpass import getpass
from app.users.enums import UserRole
from app.utils.password import validate_password


def create_admin(engine):
    print("\n=== Create Admin User ===\n")

    # Get user input securely
    email = input("Enter admin email: ").strip()
    first_name = input("Enter admin firstname: ").strip()
    last_name = input("Enter admin lastname: ").strip()

    # Get password securely without showing in terminal
    while True:
        password = getpass("Enter password: ")
        if len(password) < 12:
            print("Password must be at least 12 characters long for Admin.")
            continue
        is_valid, error_message = validate_password(password)
        if not is_valid:
            print(error_message)
            continue

        confirm_password = getpass("Confirm password: ")
        if password == confirm_password:
            break
        print("Passwords don't match. Please try again.")

    with Session(engine) as session:
        # Check if user exists
        existing_user = session.exec(
            select(User).where(User.email == email)).first()
        if existing_user:
            print(f"\nError: User with email {email} already exists")
            return

        try:
            # Create user and account
            user = UserService.create_user_account(session, UserAccountCreate(
                email=email, password=password, account=AccountCreate(
                    first_name=first_name, last_name=last_name,
                    role=UserRole.ADMIN)))

            if user:
                print(f"\nAdmin user {email} created successfully!")

        except Exception as e:
            session.rollback()
            print(f"\nError creating admin user: {str(e)}")


if __name__ == "__main__":
    # Get database URL from environment or use default
    from app.utils.database import get_database_url

    DATABASE_URL = get_database_url()

    engine = create_engine(DATABASE_URL)

    create_admin(engine)

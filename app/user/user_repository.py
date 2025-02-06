import json

from typing import Dict, Optional

from app.user.user_schema import User
from app.config import USER_DATA

from sqlalchemy.orm import Session
from database.mysql_connection import SessionLocal

class UserRepository:
    def __init__(self) -> None:
        self.users: Dict[str, dict] = self._load_users()
        self.db: Session = SessionLocal()


    def _load_users(self) -> Dict[str, Dict]:
        users = self.db.query(User).all()
        return {user.email: user.model_dump() for user in users}

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def save_user(self, user: User) -> User: 
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            for key, value in user.model_dump().items():
                setattr(existing_user, key, value)
        else:
            self.db.add(user)
        self.db.commit()
        return user

    def delete_user(self, user: User) -> User:
        db_user = self.get_user_by_email(user.email)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return user
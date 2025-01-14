from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate

class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        ## TODO
        user = None
        return user
        
    def regiser_user(self, new_user: User) -> User:
        ## TODO
        new_user = None
        return new_user

    def delete_user(self, email: str) -> User:
        ## TODO        
        deleted_user = None
        return deleted_user

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        user = self.repo.get_user_by_email(user_update.email)
        if user is None:
            raise ValueError("User not Found")
        user.password = user_update.new_password
        updated_user = self.repo.save_user(user)
        return updated_user
        
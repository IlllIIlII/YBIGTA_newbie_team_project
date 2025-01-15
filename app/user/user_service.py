from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate

class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        user = self.repo.get_user_by_email(user_login.email)
        if not user:
            raise ValueError("User not Found.")
        # 비밀번호 비교: 실제로는 해싱된 비밀번호 비교 등 보안 처리가 필요
        if user.password != user_login.password:
            raise ValueError("Invalid PW")
        return user
        
    def regiser_user(self, new_user: User) -> User:
        ## TODO
        
        """
        Registers a new user in the system.

        Args:
            new_user (User): The user object containing the details of the new user to be registered.

        Returns:
            User: The newly registered user object.

        Raises:
            ValueError: If a user with the same email already exists in the database.
        """

        existing_user = self.repo.get_user_by_email(new_user.email)
        if existing_user:
            raise ValueError("User already Exists.")
        # 새로운 사용자 생성
        new_user = self.repo.save_user(new_user)
        return new_user

    def delete_user(self, email: str) -> User:
        ## TODO   
        user = self.repo.get_user_by_email(email)
        if not user:
            raise ValueError("User not found.")
        # 사용자 삭제
        deleted_user = self.repo.delete_user(user)
        if not deleted_user:
            raise ValueError("Failed to delete user")
        return deleted_user
      

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        """
        Updates the password of an existing user

        Args:
            user_update (UserUpdate): An object of the user
        Returns:
            User: The updated user object with the new password
        Raises:
            ValueError: User not found in the database
        """
        user = self.repo.get_user_by_email(user_update.email)
        if user is None:
            raise ValueError("User not Found")
        user.password = user_update.new_password
        updated_user = self.repo.save_user(user)
        return updated_user
        
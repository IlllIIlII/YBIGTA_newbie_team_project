from app.user.user_repository import UserRepository
from app.user.user_schema import User, UserLogin, UserUpdate

class UserService:
    def __init__(self, userRepoitory: UserRepository) -> None:
        self.repo = userRepoitory

    def login(self, user_login: UserLogin) -> User:
        user = self.repo.get_user_by_email(user_login.email)
        if not user:
            raise ValueError("User not found")
        # 비밀번호 비교: 실제로는 해싱된 비밀번호 비교 등 보안 처리가 필요
        if user.password != user_login.password:
            raise ValueError("Incorrect password")
        return user
        
    def regiser_user(self, new_user: User) -> User:
        ## TODO
        existing_user = self.repo.get_user_by_email(new_user.email)
        if existing_user:
            raise ValueError("User already exists")
        # 새로운 사용자 생성
        new_user = self.repo.save_user(new_user)
        return new_user

    def delete_user(self, email: str) -> User:
        ## TODO   
        user = self.repo.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        # 사용자 삭제
        deleted_user = self.repo.delete_user(user)
        if not deleted_user:
            raise ValueError("Failed to delete user")
        return deleted_user
      

    def update_user_pwd(self, user_update: UserUpdate) -> User:
        ## TODO
        user = self.repo.get_user_by_email(user_update.email)
        if not user:
            raise ValueError("User not found")
        # 새 비밀번호로 업데이트 (실제 구현에서는 해싱 적용 필요)
        user.password = user_update.new_password
        updated_user = self.repo.save_user(user)
        return updated_user
        
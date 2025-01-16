from fastapi import APIRouter, HTTPException, Depends, status
from app.user.user_schema import User, UserLogin, UserUpdate, UserDeleteRequest
from app.user.user_service import UserService
from app.dependencies import get_user_service
from app.responses.base_response import BaseResponse

user = APIRouter(prefix="/api/user")


@user.post("/login", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    try:
        user = service.login(user_login)
        return BaseResponse(status="success", data=user, message="Login Success.") 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.post("/register", response_model=BaseResponse[User], status_code=status.HTTP_201_CREATED)
def register_user(user: User, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    Endpoint to register a new user.

    This endpoint allows the registration of a new user in the system. It validates
    if the user already exists and creates a new user if the provided email is unique.

    Args:
        user (User): The user object containing the details of the user to be registered.
        service (UserService): The user service dependency to handle user-related operations. 
            Injected automatically using FastAPI's `Depends`.

    Returns:
        BaseResponse[User]: A response object containing the status, newly registered user data, 
        and a success message.

    Raises:
        HTTPException: 
            - 400: If a user with the provided email already exists in the database.
            - 500: If an unexpected error occurs during the registration process.
    """
    try:
        new_user = service.regiser_user(user)
        return BaseResponse(status="success", data=new_user, message="User registeration success.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user.delete("/delete", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def delete_user(user_delete_request: UserDeleteRequest, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    Endpoint to delete a user.

    This endpoint handles the deletion of a user based on the provided email address.
    It verifies the user's existence and removes the user from the system.

    Args:
        user_delete_request (UserDeleteRequest): An object containing the email of the user to be deleted.
        service (UserService): The user service dependency responsible for managing user operations.

    Returns:
        BaseResponse[User]: A response object containing the status, deleted user data, 
        and a success message upon successful deletion.

    Raises:
        HTTPException: 
            - 400: If the user is not found in the database.
            - 500: If an unexpected error occurs during the deletion process.
    """
    try:
        
        deleted_user = service.delete_user(user_delete_request.email)
        return BaseResponse(status="success", data=deleted_user, message="User Deletion Success.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.put("/update-password", response_model=BaseResponse[User], status_code=status.HTTP_200_OK)
def update_user_password(user_update: UserUpdate, service: UserService = Depends(get_user_service)) -> BaseResponse[User]:
    """
    Endpoint to update the password

    Args:
        user_update (UserUpdate): An object containing the user's email and new password
        service: The user service that performs the password update

    Returns:
        BaseResponse: A response object containing the updated user information

    Raises:
        HTTPException: If the user is not found, status code 404 is returned with the error message.
    """
    user = service.update_user_pwd(user_update)
    try:
        user = service.update_user_pwd(user_update)
        return BaseResponse(status="success", data=user, message="User password update success.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

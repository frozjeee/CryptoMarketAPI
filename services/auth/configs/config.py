from fastapi import HTTPException, status


DATABASE_URL = "postgresql://admin:admin@localhost:5432/user"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

notFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
    )
credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
userAlreadyExistsException = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User already exists",
    )







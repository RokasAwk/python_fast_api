from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9]+$")
    password: str = Field(min_length=6, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {"username": "rokas", "password": "s3cret123"}
        }
    }


class RegisterResponse(BaseModel):
    message: str
    id: int
    username: str

    model_config = {
        "json_schema_extra": {
            "example": {"message": "Success", "id": 1, "username": "rokas"}
        }
    }


class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {"username": "rokas", "password": "s3cret123"}
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "example": {"access_token": "eyJhbGciOi...", "token_type": "bearer"}
        }
    }


class MeResponse(BaseModel):
    id: int
    username: str

    model_config = {
        "json_schema_extra": {
            "example": {"id": 1, "username": "rokas"}
        }
    }

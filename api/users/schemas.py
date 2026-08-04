from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int

    model_config = {
        "json_schema_extra": {
            "example": {"name": "小明", "age": 25}
        }
    }


class GetUserResponse(BaseModel):
    id: int
    name: str
    age: int

    model_config = {
        "json_schema_extra": {
            "example": {"id": 1, "name": "小明", "age": 25}
        }
    }

class GetAllUserResponse(BaseModel):
    users: list[GetUserResponse]

    model_config = {
        "json_schema_extra": {
            "example": [
                {"id": 1, "name": "小明", "age": 25},
                {"id": 2, "name": "小華", "age": 30}
            ]
        }
    }


class UpdateUserResponse(BaseModel):
    message: str
    id: int
    name: str
    age: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Success",
                "id": 1,
                "name": "小明",
                "age": 25,
            }
        }
    }

class CreateUserResponse(BaseModel):
    message: str
    id: int
    name: str
    age: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Success",
                "id": 1,
                "name": "小明",
                "age": 25,
            }
        }
    }

class DeleteUserResponse(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Success",
            }
        }
    }
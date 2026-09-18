from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class ResponseEnvelope(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"
    data: Optional[T] = None
    error: Optional[Any] = None

    @classmethod
    def ok(cls, data: T, message: str = "Success") -> "ResponseEnvelope[T]":
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str, error: Any = None) -> "ResponseEnvelope[None]":
        return cls(success=False, message=message, data=None, error=error)
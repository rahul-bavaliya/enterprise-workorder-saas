from fastapi import Query
from pydantic import BaseModel

class CommonQueryParams(BaseModel):
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination")
    limit: int = Query(20, ge=1, le=100, description="Number of items to return per page")
    search: str | None = Query(None, description="Optional search string across text fields")
    sort_by: str | None = Query(None, description="Field name to sort results by")
    descending: bool = Query(False, description="Sort order: False for ASC, True for DESC")

    @classmethod
    def depends(
        cls,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        search: str | None = Query(None),
        sort_by: str | None = Query(None),
        descending: bool = Query(False),
    ) -> "CommonQueryParams":
        return cls(skip=skip, limit=limit, search=search, sort_by=sort_by, descending=descending)
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.response import ResponseEnvelope
from app.core.query_params import CommonQueryParams
from app.core.exceptions import ExistingRecordException, NotFoundException
from app.modules.line_of_business.models import LineOfBusiness
from app.modules.line_of_business.schemas import (
    LineOfBusinessCreate,
    LineOfBusinessResponse,
    LineOfBusinessUpdate,
)

router = APIRouter(prefix="/lines-of-business", tags=["Lines of Business"])


@router.post(
    "/",
    response_model=ResponseEnvelope[LineOfBusinessResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_line_of_business(
    payload: LineOfBusinessCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new line of business with duplicate prevention rules:
    - Line of Business name must not be a duplicate (case-insensitive).
    """
    data = payload.model_dump()

    # --- DUPLICATE PREVENTION CHECK ---
    # Check if a Line of Business with the same name already exists
    duplicate_query = select(LineOfBusiness).filter(
        LineOfBusiness.lob_name.ilike(data["lob_name"])
    )

    # If you want it to only conflict if BOTH division and lob name match, use this instead:
    # duplicate_query = select(LineOfBusiness).filter(
    #     and_(
    #         LineOfBusiness.division_name.ilike(data["division_name"]),
    #         LineOfBusiness.lob_name.ilike(data["lob_name"])
    #     )
    # )

    existing_lob = (await db.execute(duplicate_query)).scalars().first()
    if existing_lob:
        raise ExistingRecordException(
            message="A Line of Business with this name already exists.",
        )
    # ----------------------------------

    lob = LineOfBusiness(**data)
    db.add(lob)
    await db.commit()
    await db.refresh(lob)

    return ResponseEnvelope.ok(
        data=lob, message="Line of Business created successfully"
    )


@router.get("/", response_model=ResponseEnvelope[list[LineOfBusinessResponse]])
async def list_lines_of_business(
    branch_id: UUID | None = None,
    params: CommonQueryParams = Depends(CommonQueryParams.depends),
    db: AsyncSession = Depends(get_db),
):
    """
    List all lines of business with pagination, optional branch filtering, search, and sorting.
    """
    query = select(LineOfBusiness)

    if branch_id:
        query = query.filter(LineOfBusiness.branch_id == branch_id)

    if params.search:
        query = query.filter(LineOfBusiness.lob_name.ilike(f"%{params.search}%"))

    query = query.order_by(LineOfBusiness.lob_name.asc())
    query = query.offset(params.skip).limit(params.limit)

    result = await db.execute(query)
    lobs = result.scalars().all()

    return ResponseEnvelope.ok(
        data=lobs, message="Fetched lines of business successfully"
    )


@router.get("/{lob_id}", response_model=ResponseEnvelope[LineOfBusinessResponse])
async def get_line_of_business(lob_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single line of business by its UUID.
    """
    result = await db.execute(
        select(LineOfBusiness).filter(LineOfBusiness.id == lob_id)
    )
    lob = result.scalars().first()

    if not lob:
        raise NotFoundException(message="Line of business not found")

    return ResponseEnvelope.ok(
        data=lob, message="Line of business fetched successfully"
    )


@router.patch("/{lob_id}", response_model=ResponseEnvelope[LineOfBusinessResponse])
async def update_line_of_business(
    lob_id: UUID, payload: LineOfBusinessUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Partially update an existing line of business.
    """
    result = await db.execute(
        select(LineOfBusiness).filter(LineOfBusiness.id == lob_id)
    )
    lob = result.scalars().first()

    if not lob:
        raise NotFoundException(message="Line of business not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lob, key, value)

    await db.commit()
    await db.refresh(lob)

    return ResponseEnvelope.ok(
        data=lob, message="Line of business updated successfully"
    )


@router.delete("/{lob_id}", response_model=ResponseEnvelope[LineOfBusinessResponse])
async def delete_line_of_business(lob_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Deactivate a line of business from the system.
    """
    lob = await db.get(LineOfBusiness, lob_id)
    if not lob:
        raise NotFoundException(message="Line Of Business not found")

    # Fixed: Replaced undefined NotActiveException with standard FastAPI HTTPException
    if not lob.is_active:
        raise NotActiveException(message="Line of business is not active")

    setattr(lob, "is_active", False)

    await db.commit()
    await db.refresh(lob)

    return ResponseEnvelope.ok(
        data=lob, message="Line of business deactivated successfully"
    )

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.response import ResponseEnvelope
from app.core.query_params import CommonQueryParams
from app.core.exceptions import NotFoundException
from app.modules.branch.models import Branch
from app.modules.branch.schemas import BranchCreate, BranchResponse, BranchUpdate

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.post("/", response_model=ResponseEnvelope[BranchResponse], status_code=status.HTTP_201_CREATED)
async def create_branch(payload: BranchCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new branch.
    """
    data = payload.model_dump()
    if data.get("website_url"):
        data["website_url"] = str(data["website_url"])

    branch = Branch(**data)
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    
    return ResponseEnvelope.ok(data=branch, message="Branch created successfully")


@router.get("/", response_model=ResponseEnvelope[list[BranchResponse]])
async def list_branches(
    params: CommonQueryParams = Depends(CommonQueryParams.depends),
    db: AsyncSession = Depends(get_db),
):
    """
    List all branches with pagination, search, and predictable ordering.
    """
    query = select(Branch)

    # Apply search filter if provided
    if params.search:
        query = query.filter(Branch.name.ilike(f"%{params.search}%"))

    # Apply pagination using the query params utility
    query = query.offset(params.skip).limit(params.limit)

    result = await db.execute(query)
    branches = result.scalars().all()

    return ResponseEnvelope.ok(data=branches, message="Fetched branches successfully")


@router.get("/{branch_id}", response_model=ResponseEnvelope[BranchResponse])
async def get_branch(branch_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single branch by its UUID.
    """
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise NotFoundException(message="Branch not found")
        
    return ResponseEnvelope.ok(data=branch, message="Branch fetched successfully")


@router.patch("/{branch_id}", response_model=ResponseEnvelope[BranchResponse])
async def update_branch(
    branch_id: UUID, payload: BranchUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Partially update an existing branch's details.
    """
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise NotFoundException(message="Branch not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "website_url" in update_data and update_data["website_url"] is not None:
        update_data["website_url"] = str(update_data["website_url"])

    for key, value in update_data.items():
        setattr(branch, key, value)

    await db.commit()
    await db.refresh(branch)
    
    return ResponseEnvelope.ok(data=branch, message="Branch updated successfully")


@router.delete("/{branch_id}", response_model=ResponseEnvelope[None])
async def delete_branch(branch_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Delete a branch from the system.
    """
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise NotFoundException(message="Branch not found")

    await db.delete(branch)
    await db.commit()
    
    return ResponseEnvelope.ok(data=None, message="Branch deleted successfully")
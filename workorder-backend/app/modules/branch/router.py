from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.modules.branch.models import Branch

# Make sure to double-check if your schemas are in branch.schemas based on your folder structure
from app.modules.branch.schemas import BranchCreate, BranchResponse, BranchUpdate

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
async def create_branch(payload: BranchCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new branch.
    """
    # Convert Pydantic fields (like HttpUrl) to strings if needed for SQLAlchemy compatibility
    data = payload.model_dump()
    if data.get("website_url"):
        data["website_url"] = str(data["website_url"])

    branch = Branch(**data)
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch


@router.get("/", response_model=list[BranchResponse])
async def list_branches(db: AsyncSession = Depends(get_db)):
    """
    List all branches.
    """
    query = select(Branch)

    # Order by the new sequence number so lists come back predictable
    query = query.order_by(Branch.number.asc())

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch(branch_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single branch by its UUID.
    """
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found"
        )
    return branch


@router.patch("/{branch_id}", response_model=BranchResponse)
async def update_branch(
    branch_id: UUID, payload: BranchUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Partially update an existing branch's details.
    """
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found"
        )

    # Extract only the fields explicitly sent in the patch payload body
    update_data = payload.model_dump(exclude_unset=True)

    # Cast Pydantic's specialized URL object to a standard string for SQLAlchemy
    if "website_url" in update_data and update_data["website_url"] is not None:
        update_data["website_url"] = str(update_data["website_url"])

    for key, value in update_data.items():
        setattr(branch, key, value)

    await db.commit()
    await db.refresh(branch)
    return branch


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch(branch_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Delete a branch from the system.
    """
    branch = await db.get(Branch, branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found"
        )

    await db.delete(branch)
    await db.commit()
    return None

# app/api/v1/endpoints/branch.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.response import ResponseEnvelope
from app.core.exceptions import NotFoundException
from app.api.v1.schemas.branch import BranchCreate, BranchResponse, BranchUpdate
from app.api.v1.services.branch import BranchService
import io
import csv
from fastapi import UploadFile, File

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseEnvelope[BranchResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_branch(
    *,
    branch_in: BranchCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseEnvelope[BranchResponse]:
    """
    Create a new branch.
    """
    service = BranchService(db)
    branch = await service.create(obj_in=branch_in)
    return ResponseEnvelope[BranchResponse].ok(
        data=BranchResponse.model_validate(branch),
        message="Branch created successfully",
    )


@router.get("/", response_model=ResponseEnvelope[List[BranchResponse]])
async def read_branches(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> ResponseEnvelope[List[BranchResponse]]:
    """
    Retrieve branches.
    """
    service = BranchService(db)
    branches = await service.get_multi(skip=skip, limit=limit)
    branch_responses = [BranchResponse.model_validate(b) for b in branches]
    return ResponseEnvelope[List[BranchResponse]].ok(
        data=branch_responses, message="Branches retrieved successfully"
    )


@router.get("/{branch_id}", response_model=ResponseEnvelope[BranchResponse])
async def read_branch(
    *,
    branch_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseEnvelope[BranchResponse]:
    """
    Get a specific branch by id.
    """
    service = BranchService(db)
    branch = await service.get(id=branch_id)
    if not branch:
        raise NotFoundException(message="Branch not found")
    return ResponseEnvelope[BranchResponse].ok(
        data=BranchResponse.model_validate(branch),
        message="Branch retrieved successfully",
    )


@router.patch("/{branch_id}", response_model=ResponseEnvelope[BranchResponse])
async def update_branch(
    *,
    branch_id: UUID,
    branch_in: BranchUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseEnvelope[BranchResponse]:
    """
    Update a branch.
    """
    service = BranchService(db)
    branch = await service.get(id=branch_id)
    if not branch:
        raise NotFoundException(message="Branch not found")
    updated_branch = await service.update(db_obj=branch, obj_in=branch_in)
    return ResponseEnvelope[BranchResponse].ok(
        data=BranchResponse.model_validate(updated_branch),
        message="Branch updated successfully",
    )


@router.delete("/{branch_id}", response_model=ResponseEnvelope[BranchResponse])
async def delete_branch(
    *,
    branch_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> (
    ResponseEnvelope[ResponseEnvelope[BranchResponse] | None]
    | ResponseEnvelope[BranchResponse]
):
    """
    Delete a branch.
    """
    service = BranchService(db)
    branch = await service.get(id=branch_id)
    if not branch:
        raise NotFoundException(message="Branch not found")
    deleted_branch = await service.remove(id=branch_id)
    return ResponseEnvelope[BranchResponse].ok(
        data=BranchResponse.model_validate(deleted_branch),
        message="Branch deleted successfully",
    )


@router.post(
    "/bulk-upload",
    response_model=ResponseEnvelope[dict],
    status_code=status.HTTP_201_CREATED,
)
async def bulk_upload_branches(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> ResponseEnvelope[dict]:
    """
    Bulk upload branches from a CSV file.
    """
    if not file.filename.endswith(".csv"):
        return ResponseEnvelope[dict].error(
            code="INVALID_FILE_FORMAT", message="Please upload a valid CSV file."
        )

    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    service = BranchService(db)
    success_count = 0
    errors = []

    for row in reader:
        try:
            # Map your CSV columns to your BranchCreate schema fields.
            # Adjust keys below to match exact column names inside your Branches.csv
            branch_in = BranchCreate(
                name=row.get("Branch Name"),
                number=int(row.get("Branch Number", 0)),
                lob_id=row.get("lob_id"),
                business_id=row.get("business_id"),
                branch_manager_id=row.get("branch_manager_id") or None,
                address1=row.get("Address1"),
                address2=None,
                city=row.get("Branch City"),
                postal_code=row.get("PostalCode"),
                province=row.get("Branch Province"),
                country=row.get("Branch Country"),
                latitude=float(row.get("Latitude", 0.0)),
                longitude=float(row.get("Longitude", 0.0)),
                region=row.get("Region Name"),
                phone=row.get("phone"),
                email=row.get("email"),
                website_url=row.get("website_url"),
                contact_person=row.get("contact_person"),
                division_name=row.get("division_name"),
                is_active=str(row.get("is_active", "True")).lower()
                in ("true", "1", "yes"),
            )
            await service.create(obj_in=branch_in)
            success_count += 1
        except Exception as e:
            errors.append({"row": row, "error": str(e)})

    return ResponseEnvelope[dict].ok(
        data={"success_count": success_count, "errors": errors},
        message=f"Successfully uploaded {success_count} branches.",
    )

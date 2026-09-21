# app/modules/Make_product_model/router.py
import json
from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.response import ResponseEnvelope
from app.core.query_params import CommonQueryParams
from app.core.exceptions import NotFoundException
from app.modules.make_product_model.models import MakeProductModel
from app.modules.make_product_model.schemas import (
    MakeProductModelCreate,
    MakeProductModelResponse,
    MakeProductModelUploadSummary,
)

router = APIRouter(prefix="/make-product-model", tags=["Make Product Model Catalog"])


@router.post(
    "/upload-json/",
    response_model=ResponseEnvelope[MakeProductModelUploadSummary],
    status_code=status.HTTP_200_OK,
)
async def upload_make_product_model_json(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    """
    Bulk upload the JSON equipment catalog file.
    Prevents duplicates using PRODUCT_ID (handled as int).
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid .json file.",
        )

    try:
        contents = await file.read()
        data = json.loads(contents.decode("utf-8"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse JSON content: {str(e)}",
        )

    items = list(data.values()) if isinstance(data, dict) else data

    inserted_count = 0
    updated_count = 0
    processed_count = 0

    for val in items:
        raw_product_id = val.get("PRODUCT_ID")
        if raw_product_id is None:
            continue

        try:
            product_id = int(raw_product_id)
        except (ValueError, TypeError):
            continue  # Skip rows where product_id cannot be parsed as an integer

        processed_count += 1

        result = await db.execute(
            select(MakeProductModel).where(MakeProductModel.product_id == product_id)
        )
        existing_record = result.scalars().first()

        if existing_record:
            existing_record.model_id = val.get("MODEL_ID")
            existing_record.category_id = val.get("CATEGORY_ID")
            existing_record.sub_category_id = val.get("SUB_CATEGORY_ID")
            existing_record.make = val.get("MAKE")
            existing_record.model = val.get("MODEL")
            existing_record.decal_model = val.get("DECALMODEL")
            existing_record.category = val.get("CATEGORY")
            existing_record.sub_category = val.get("SUB_CATEGORY")
            existing_record.division = val.get("DIVISION")
            existing_record.jd_product_family = val.get("JD_PRODUCT_FAMILY")
            updated_count += 1
        else:
            new_item = MakeProductModel(
                product_id=product_id,
                model_id=val.get("MODEL_ID"),
                category_id=val.get("CATEGORY_ID"),
                sub_category_id=val.get("SUB_CATEGORY_ID"),
                make=val.get("MAKE"),
                model=val.get("MODEL"),
                decal_model=val.get("DECALMODEL"),
                category=val.get("CATEGORY"),
                sub_category=val.get("SUB_CATEGORY"),
                division=val.get("DIVISION"),
                jd_product_family=val.get("JD_PRODUCT_FAMILY"),
            )
            db.add(new_item)
            inserted_count += 1

    await db.commit()

    summary = MakeProductModelUploadSummary(
        total_processed=processed_count,
        inserted=inserted_count,
        updated=updated_count,
        message="Make product model catalog processed and uploaded successfully.",
    )

    return ResponseEnvelope.ok(
        data=summary, message="Catalog synchronized successfully"
    )


@router.post(
    "/",
    response_model=ResponseEnvelope[MakeProductModelResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_make_product_model(
    payload: MakeProductModelCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a single individual equipment record manually.
    Verifies that the `product_id` is unique to prevent duplicate rows.
    """
    # Check if a record with this product_id already exists
    result = await db.execute(
        select(MakeProductModel).where(
            MakeProductModel.product_id == payload.product_id
        )
    )
    existing_record = result.scalars().first()

    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An equipment record with product_id '{payload.product_id}' already exists.",
        )

    # Initialize new model (db model handles auto-generating the primary 'id' key like MPM-XXXXXXXX)
    new_record = MakeProductModel(
        product_id=payload.product_id,
        model_id=payload.model_id,
        category_id=payload.category_id,
        sub_category_id=payload.sub_category_id,
        make=payload.make,
        model=payload.model,
        decal_model=payload.decal_model,
        category=payload.category,
        sub_category=payload.sub_category,
        division=payload.division,
        jd_product_family=payload.jd_product_family,
    )

    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)

    return ResponseEnvelope.ok(
        data=new_record, message="Equipment record created successfully"
    )


@router.get("/", response_model=ResponseEnvelope[list[MakeProductModelResponse]])
async def list_make_product_models(
    make: str | None = None,
    category: str | None = None,
    params: CommonQueryParams = Depends(CommonQueryParams.depends),
    db: AsyncSession = Depends(get_db),
):
    """
    List all equipment models with optional filtering by make/category, search, and pagination.
    """
    query = select(MakeProductModel)

    if make:
        query = query.filter(MakeProductModel.make.ilike(f"%{make}%"))
    if category:
        query = query.filter(MakeProductModel.category.ilike(f"%{category}%"))
    if params.search:
        query = query.filter(MakeProductModel.model.ilike(f"%{params.search}%"))

    query = query.order_by(MakeProductModel.make.asc())
    query = query.offset(params.skip).limit(params.limit)

    result = await db.execute(query)
    models = result.scalars().all()

    return ResponseEnvelope.ok(
        data=models, message="Equipment models fetched successfully"
    )


@router.get("/{record_id}", response_model=ResponseEnvelope[MakeProductModelResponse])
async def get_make_product_model(record_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single individual equipment record by its unique primary key ID (e.g., MPM-XXXXXXXX).
    """
    result = await db.execute(
        select(MakeProductModel).filter(MakeProductModel.id == record_id)
    )
    record = result.scalars().first()

    if not record:
        raise NotFoundException(message="Equipment record not found")

    return ResponseEnvelope.ok(
        data=record, message="Equipment record fetched successfully"
    )


@router.delete("/{record_id}", response_model=ResponseEnvelope[None])
async def delete_make_product_model(record_id: str, db: AsyncSession = Depends(get_db)):
    """
    Delete a single individual equipment record from the system.
    """
    result = await db.execute(
        select(MakeProductModel).filter(MakeProductModel.id == record_id)
    )
    record = result.scalars().first()

    if not record:
        raise NotFoundException(message="Equipment record not found")

    await db.delete(record)
    await db.commit()

    return ResponseEnvelope.ok(
        data=None, message="Equipment record deleted successfully"
    )

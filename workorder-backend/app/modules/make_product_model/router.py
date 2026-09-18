# app/modules/Make_product_model/router.py
import json
import asyncio
from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.modules.make_product_model.models import MakeProductModel

router = APIRouter(prefix="/make-product-model", tags=["Make Product Model Catalog"])


@router.post("/stream-upload-json/")
async def stream_upload_make_product_model_json(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Uploads the JSON file, maps all comprehensive metadata fields, 
    and streams live insertion progress counters via Server-Sent Events (SSE).
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a valid .json file."
        )

    try:
        contents = await file.read()
        data = json.loads(contents.decode("utf-8"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse JSON content: {str(e)}"
        )

    items = list(data.values()) if isinstance(data, dict) else data
    total_items = len(items)

    async def event_generator():
        inserted_count = 0
        updated_count = 0
        processed_count = 0

        yield f"data: {json.dumps({'status': 'started', 'total': total_items})}\n\n"

        for val in items:
            product_id = str(val.get("PRODUCT_ID"))
            if not product_id:
                continue

            processed_count += 1

            # Check if record already exists by product_id to prevent duplicates
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

            progress_payload = {
                "processed": processed_count,
                "inserted": inserted_count,
                "updated": updated_count,
                "total": total_items,
                "current_model": val.get("MODEL")
            }
            yield f"data: {json.dumps(progress_payload)}\n\n"
            
            await asyncio.sleep(0.001)

        final_payload = {
            'status': 'completed',
            'total_processed': processed_count,
            'inserted': inserted_count,
            'updated': updated_count
        }
        yield f"data: {json.dumps(final_payload)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
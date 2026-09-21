# scripts/seed_branches.py
import asyncio
import csv
import os
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal
from app.api.v1.schemas.branch import BranchCreate
from app.api.v1.services.branch import BranchService


async def seed_branches(csv_file_path: str = "../files/branches.csv") -> None:
    """
    Reads the Branches CSV file and asynchronously bulk inserts records
    into the database using BranchService and BranchCreate schema.
    """
    if not os.path.exists(csv_file_path):
        if os.path.exists("files/branches.csv"):
            csv_file_path = "files/branches.csv"
        elif os.path.exists("Branches.csv"):
            csv_file_path = "Branches.csv"
        else:
            print(f"❌ Error: CSV file not found at path: {csv_file_path}")
            return

    success_count = 0
    error_count = 0

    async with SessionLocal() as db:
        service = BranchService(db)

        try:
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                print(f"📂 Successfully loaded {len(rows)} rows from {csv_file_path}.")

                for index, row in enumerate(rows):
                    try:

                        def get_float(val):
                            if not val or val.strip() == "" or val.strip() == "-":
                                return None
                            return float(val.replace("'", ""))

                        def get_int(val):
                            if not val or val.strip() == "" or val.strip() == "-":
                                return None
                            return int(val.strip())

                        # Instantiating BranchCreate matching your exact schema fields
                        branch_in = BranchCreate(
                            name=row.get("Branch Name", "").strip() or "Unnamed Branch",
                            number=get_int(row.get("Branch Number")),
                            join_key=get_int(row.get("1")) or (index + 1),
                            address1=row.get("Address1", "").strip() or None,
                            address2=row.get("Address2", "").strip() or None,
                            city=row.get("Branch City", "").strip() or "Unknown",
                            postal_code=row.get("PostalCode", "").strip() or "N/A",
                            province=row.get("Branch Province", "").strip() or "N/A",
                            country=row.get("Branch Country", "").strip() or "CA",
                            latitude=get_float(row.get("Latitude")),
                            longitude=get_float(row.get("Longitude")),
                            region=row.get("Region Name", "").strip() or None,
                            phone=row.get("Telephone1", "").strip() or None,
                            email=row.get("Email", "").strip() or None,
                            website_url=row.get("Website", "").strip() or None,
                            contact_person=row.get("ContactPerson", "").strip() or None,
                            division_name=row.get("Division Name", "").strip() or None,
                            lob_name=str(row.get("LOBName", "")).split(",")[0].strip()
                            or None,
                            is_active=True,
                        )

                        await service.create(obj_in=branch_in)
                        success_count += 1
                        print(
                            f"[{index + 1}/{len(rows)}] ✅ Inserted: {branch_in.name}"
                        )

                    except Exception as e:
                        error_count += 1
                        print(
                            f"[{index + 1}/{len(rows)}] ⚠️ Failed row {index + 1}: {e}"
                        )

        except Exception as e:
            print(f"❌ Error opening or reading CSV file: {e}")
            return

    print("\n--- Bulk Seed Execution Summary ---")
    print(f"✨ Successfully inserted: {success_count} branches")
    print(f"❌ Failed / Skipped: {error_count} rows")


if __name__ == "__main__":
    asyncio.run(seed_branches())

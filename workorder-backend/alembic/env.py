""" alembic/env.py
This is the Alembic environment script for handling database migrations.
It sets up the database connection and runs migrations in both offline and online modes."""

import asyncio
import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Add the parent directory to sys.path so 'app' can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import your application's Base, models, and settings config
from app.core.database import Base
from app.core.config import settings
from app.modules.branch.models import Branch
from app.modules.tenant.models import Tenant
from app.modules.work_order.models import Asset, WorkOrder, WorkOrderTask

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url() -> str:
    """Retrieve database URL and ensure it uses the async driver for Alembic."""
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    if "postgresql://" in db_url and "+asyncpg" not in db_url:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    return db_url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Create an AsyncEngine and associate a connection with the context."""
    database_url = get_url()

    connectable = create_async_engine(
        database_url,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode using asyncio."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
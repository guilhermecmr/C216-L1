import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/faculdade_db"
)

async def get_connection():
    return await asyncpg.connect(DATABASE_URL)
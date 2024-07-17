from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

ASYNC_SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:11597@localhost/fast_lms'

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def async_get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()

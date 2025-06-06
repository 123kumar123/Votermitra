
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 👇 Replace with your actual MySQL connection details
DATABASE_URL = "mysql+asyncmy://u522804379_Election123:Votermitra_123@auth-db1880.hstgr.io:3306/u522804379_Election"


# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async sessionmaker
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from . import settings

# Create database engine
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Create async session maker
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

###
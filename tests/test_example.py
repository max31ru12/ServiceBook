import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User

pytestmark = pytest.mark.anyio


async def test_database_setup(session: AsyncSession):
    result = await session.execute(text("SELECT 1"))
    assert result.scalar() == 1


async def test_client_request(client):
    response = client.get("/")
    assert response.status_code == 200


async def test_register(client, session):
    register_data = {
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    response = client.post("/auth/register", json=register_data)
    data = await session.execute(select(User))
    print(data.scalars().all())
    assert data is not None
    assert response.status_code == 201

import pytest
import httpx

@pytest.mark.asyncio
async def test_create_book():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post("/books/", json={"title": "New Book", "author": "Author"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Book"
        assert data["author"] == "Author"

@pytest.mark.asyncio
async def test_get_books():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

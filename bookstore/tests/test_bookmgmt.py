import pytest
from unittest.mock import Mock
from bookmgmt import create_book, update_book, delete_book, get_book_by_id, get_all_books
from fastapi import HTTPException
from database import Book

@pytest.mark.asyncio
async def test_create_book_success():
    mock_db = Mock()
    book_data = Book(id=1, title="Test Book")
    
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    result = await create_book(book_data, mock_db)
    assert result.id == book_data.id
    assert result.title == book_data.title
    mock_db.add.assert_called_once_with(book_data)
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_book_success():
    mock_db = Mock()
    existing_book = Book(id=1, title="Old Title")
    update_data = Book(id=1, title="Updated Title")

    mock_db.query.return_value.filter.return_value.first.return_value = existing_book
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    result = await update_book(1, update_data, mock_db)
    assert result.title == "Updated Title"
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_book_not_found():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        await update_book(1, Book(id=1, title="Updated Title"), mock_db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

@pytest.mark.asyncio
async def test_delete_book_success():
    mock_db = Mock()
    existing_book = Book(id=1, title="Test Book")
    
    mock_db.query.return_value.filter.return_value.first.return_value = existing_book
    mock_db.commit = Mock()
    
    result = await delete_book(1, mock_db)
    assert result['message'] == "Book deleted successfully"
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_delete_book_not_found():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        await delete_book(1, mock_db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

@pytest.mark.asyncio
async def test_get_book_by_id_success():
    mock_db = Mock()
    existing_book = Book(id=1, title="Test Book")

    mock_db.query.return_value.filter.return_value.first.return_value = existing_book
    
    result = await get_book_by_id(1, mock_db)
    assert result.id == existing_book.id
    assert result.title == existing_book.title

@pytest.mark.asyncio
async def test_get_book_by_id_not_found():
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        await get_book_by_id(1, mock_db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Book not found"

@pytest.mark.asyncio
async def test_get_all_books_success():
    mock_db = Mock()
    book_list = [Book(id=1, title="Book 1"), Book(id=2, title="Book 2")]
    
    mock_db.query.return_value.all.return_value = book_list
    
    result = await get_all_books(mock_db)
    assert len(result) == 2
    assert result[0].title == "Book 1"

@pytest.mark.asyncio
async def test_get_all_books_empty():
    mock_db = Mock()
    mock_db.query.return_value.all.return_value = []

    result = await get_all_books(mock_db)
    assert len(result) == 0

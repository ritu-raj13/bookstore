# Bookstore API Test Automation

## How to run the tests locally:

### Unit Tests:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov

2. Run Unit Tests with coverage:
pytest --cov=bookmgmt tests/test_bookmgmt.py

### Integration Tests:
1. Start the FastAPI server:
uvicorn app.main:app --reload

2. Run Integration Tests:
pytest tests/test_integration.py

Testing Strategy:
Unit Tests: We used mocking to isolate database connections and tested the core logic of the FastAPI app.
Integration Tests: We used httpx to test the API endpoints' end-to-end functionality.


Challenges:
Mocking MongoDB connections to ensure the unit tests are independent of actual database operations.
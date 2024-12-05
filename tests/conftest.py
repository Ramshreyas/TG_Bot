import pytest
import asyncio
from db.database import engine, init_db

def pytest_addoption(parser):
    parser.addoption("--test-code", action="store", default="TEST_MESSAGE_123",
                    help="Test code to search for in messages")

@pytest.fixture
def test_code(request):
    return request.config.getoption("--test-code")

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
def setup_database():
    """Initialize the database before testing"""
    init_db()
    yield
    # Clean up can be added here if needed

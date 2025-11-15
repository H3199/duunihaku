import pytest

@pytest.fixture(scope="session")
def base_url():
    return "http://10.0.0.1:8501"

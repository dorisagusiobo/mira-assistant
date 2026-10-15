import os
import tempfile
from pathlib import Path

# Point the app at a throwaway database before it's imported, since the engine
# is created at import time. Never touches the developer's mira.db.
_DB = Path(tempfile.mkdtemp(prefix="mira-test-")) / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{_DB}"
os.environ["OPENAI_API_KEY"] = ""

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client

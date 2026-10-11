from fastapi.testclient import TestClient
from sysdiag.api.main import app

client = TestClient(app)


def test_missing_process_returns_404():
    response = client.get("/processes/99999999")

    assert response.status_code == 404
    assert response.json() == {
    "detail": "Process with PID 99999999 Not Found"
    }
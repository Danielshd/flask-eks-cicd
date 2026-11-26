from app import app


def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_home():
    response = client().get("/")
    assert response.status_code == 200


def test_health():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_users_without_database(monkeypatch):
    monkeypatch.delenv("DB_HOST", raising=False)
    response = client().get("/users")
    assert response.status_code == 503

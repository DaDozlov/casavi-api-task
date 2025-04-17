import json

from src import auth


def test_get_token_happy_path(monkeypatch, tmp_path):
    """get_token() stores the file and returns the token string."""

    # fake env
    monkeypatch.setenv("CASAVI_API_KEY", "dummy_key")
    monkeypatch.setenv("CASAVI_API_SECRET", "dummy_secret")

    # fake HTTP
    def _fake_post(url, json):
        class _Resp:
            def raise_for_status(self):
                ...

            def json(self):
                return {"token": "abc‑123", "expiresAt": "2099‑01‑01T00:00:00Z"}

        assert url.endswith("/authenticate")
        assert json == {"key": "dummy_key", "secret": "dummy_secret"}
        return _Resp()

    monkeypatch.setattr(auth.requests, "post", _fake_post)

    # use a temp file instead of the real token.json
    tmp_token = tmp_path / "token.json"
    monkeypatch.setattr(auth, "TOKEN_FILE", tmp_token)

    token = auth.get_token()
    assert token == "abc‑123"
    data = json.loads(tmp_token.read_text())
    assert data["token"] == "abc‑123"
    assert data["fetchedAt"]


def test_load_token_from_file(tmp_path, monkeypatch):
    p = tmp_path / "token.json"
    p.write_text(json.dumps({"token": "xyz"}))
    monkeypatch.chdir(tmp_path)
    assert auth.load_token_from_file() == "xyz"

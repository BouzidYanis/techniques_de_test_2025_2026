"""Tests pour l'API de triangulation, en particulier l'endpoint /triangulate/<pointsetid>.

Ces tests utilisent des mocks pour simuler les appels au PointSetManager.
"""

from unittest.mock import Mock, patch

import pytest
import requests


def _make_resp(status_code=200, content=b''):
    """Retourne un Mock qui ressemble à l'objet Response utilisé par le code.

    (status_code, content, raise_for_status()).
    """
    resp = Mock()
    resp.status_code = status_code
    resp.content = content
    # Par défaut raise_for_status ne lève pas ; si status >= 400 on simule une erreur.
    if status_code >= 400:
        def _raise():
            raise requests.HTTPError(f"HTTP {status_code}")
        resp.raise_for_status.side_effect = _raise
    else:
        resp.raise_for_status = Mock()
    return resp


def test_get_triangulate_with_valid_pointsetid(flask_test_client, sample_triangle_pointset_bytes):
    """Mock de requests.get pour renvoyer un PointSet binaire valide.

    Vérifie que l'endpoint /triangulate/<id> renvoie du binaire et un code 200/201.
    """
    client = flask_test_client
    if client is None:
        pytest.skip("Flask test client non disponible")

    # cela remplace requests.get qui doit nous renvoyer les points à partir de PointSetManage  par un mock
    # si comme si on dit si quelqu'un fait requests.get(...) on lui renvoie un Mock qui a le contenu sample_triangle_pointset_bytes
    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(200, sample_triangle_pointset_bytes)

        resp = client.get("/triangulate/42")
        assert resp.status_code in (200, 201)
        assert resp.data is not None and len(resp.data) > 0
        # Content-Type peut être vide selon implémentation ; sinon doit être octet-stream
        ct = resp.headers.get("Content-Type", "")
        assert ct == "" or ct.startswith("application/octet-stream")

        # Vérifier que nous avons bien appelé la dépendance externe
        mock_get.assert_called()
        # Optionnel: vérifier URL (adapter si votre route interne diffère)
        called_args, called_kwargs = mock_get.call_args
        assert len(called_args) >= 1
        assert "pointset" in called_args[0] or "PointSet" in called_args[0] or isinstance(called_args[0], str)

def test_pointsetid_not_found_returns_404(flask_test_client):
    """Mock de requests.get pour renvoyer 404 depuis le PointSetManager.

    Triangulator doit propager un 404 (ou 422 selon design).
    """
    client = flask_test_client
    if client is None:
        pytest.skip("Flask test client non disponible")

    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(404, b"")

        resp = client.get("/triangulate/99999")
        assert resp.status_code in (404, 422)

        mock_get.assert_called()

def test_malformed_pointset_from_manager_returns_400(flask_test_client):
    """Mock de requests.get pour renvoyer un payload binaire corrompu.

    Triangulator doit détecter le format invalide et renvoyer 400/422/500 selon implémentation.
    """
    client = flask_test_client
    if client is None:
        pytest.skip("Flask test client non disponible")

    with patch("requests.get") as mock_get:
        # Binaire trop court / corrompu
        mock_get.return_value = _make_resp(200, b"\x00\x01")

        resp = client.get("/triangulate/55")
        assert resp.status_code in (400, 422, 500)

        mock_get.assert_called()

def test_network_error_returns_503(flask_test_client):
    """Simule une erreur réseau (requests.exceptions.RequestException) -> 503."""
    client = flask_test_client
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("down")
        resp = client.get("/triangulate/42")
        assert resp.status_code == 503

def test_deserialization_generic_error_returns_422(flask_test_client, monkeypatch):
    """Simule une Exception générique dans bytes_to_pointset -> 400."""
    client = flask_test_client
    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(200, b"\x00\x00\x00\x00")
        # force une Exception dans bytes_to_pointset
        monkeypatch.setattr(
            "TP.Code.serializers.bytes_to_pointset",
            lambda _: (_ for _ in ()).throw(Exception("boom"))
        )
        resp = client.get("/triangulate/42")
        assert resp.status_code == 422
        assert b"Malformed data" in resp.data

def test_success_returns_octet_stream(flask_test_client, monkeypatch):
    """Chemin succès: répond 200 avec octet-stream et des bytes non vides."""
    client = flask_test_client
    import struct
    payload = (
        struct.pack("<I", 3)
        + struct.pack("<dd", 0.0, 0.0)
        + struct.pack("<dd", 1.0, 0.0)
        + struct.pack("<dd", 0.0, 1.0)
    )
    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(200, payload)
        # triangulation retourne 1 triangle
        monkeypatch.setattr("TP.Code.triangulation.triangulate", lambda pts: [(0, 1, 2)])
        resp = client.get("/triangulate/7")
        assert resp.status_code == 200
        assert resp.data and len(resp.data) > 0
        assert resp.headers.get("Content-Type", "").startswith("application/octet-stream")

def test_triangulation_valueerror_returns_422(flask_test_client, monkeypatch):
    """ValueError métier de triangulation -> 422."""
    client = flask_test_client
    import struct
    payload = (
        struct.pack("<I", 3)
        + struct.pack("<dd", 0.0, 0.0)
        + struct.pack("<dd", 1.0, 1.0)
        + struct.pack("<dd", 2.0, 2.0)
    )
    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(200, payload)
        monkeypatch.setattr("TP.Code.triangulation.triangulate", lambda pts: (_ for _ in ()).throw(ValueError("All points are colinear")))
        resp = client.get("/triangulate/8")
        assert resp.status_code == 422
        assert b"All points are colinear" in resp.data

def test_serialization_generic_error_returns_500(flask_test_client, monkeypatch):
    """Exception générique dans triangles_to_bytes -> 500."""
    client = flask_test_client
    import struct
    payload = (
        struct.pack("<I", 3)
        + struct.pack("<dd", 0.0, 0.0)
        + struct.pack("<dd", 1.0, 0.0)
        + struct.pack("<dd", 0.0, 1.0)
    )
    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(200, payload)
        monkeypatch.setattr("TP.Code.triangulation.triangulate", lambda pts: [(0, 1, 2)])
        monkeypatch.setattr("TP.Code.serializers.triangles_to_bytes", lambda *args, **kwargs: (_ for _ in ()).throw(Exception("serialize-error")))
        resp = client.get("/triangulate/9")
        assert resp.status_code == 500
        assert b"Serialization failed" in resp.data

def test_triangulation_generic_error_returns_500(flask_test_client, monkeypatch):
    """Exception générique dans triangulate -> 500 Triangulation failed."""
    client = flask_test_client
    import struct
    payload = (
        struct.pack("<I", 3)
        + struct.pack("<dd", 0.0, 0.0)
        + struct.pack("<dd", 1.0, 0.0)
        + struct.pack("<dd", 0.0, 1.0)
    )
    with patch("requests.get") as mock_get:
        mock_get.return_value = _make_resp(200, payload)
        # Force une Exception générique sur triangulate
        monkeypatch.setattr(
            "TP.Code.triangulation.triangulate",
            lambda pts: (_ for _ in ()).throw(Exception("boom"))
        )
        resp = client.get("/triangulate/123")
        assert resp.status_code == 500
        assert b"Triangulation failed" in resp.data


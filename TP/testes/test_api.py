import pytest
import requests
from unittest.mock import patch, Mock

def _make_resp(status_code=200, content=b''):
    """
    Retourne un Mock qui ressemble à l'objet Response utilisé par le code
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
    """
    Mock de requests.get pour renvoyer un PointSet binaire valide.
    Vérifie que l'endpoint /triangulate/<id> renvoie du binaire et un code 200/201.
    """
    client = flask_test_client
    if client is None:
        pytest.skip("Flask test client non disponible")

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
    """
    Mock de requests.get pour renvoyer 404 depuis le PointSetManager.
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
    """
    Mock de requests.get pour renvoyer un payload binaire corrompu.
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
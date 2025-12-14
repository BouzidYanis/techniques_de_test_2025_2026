"""Fixtures communes pour les tests."""

import os
import struct
import sys

import pytest

from TP.Code.app import app

# S'assurer que les imports TP.Code.* fonctionnent
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)



@pytest.fixture
def flask_test_client():
    """Fixture pour le client de test Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client



@pytest.fixture
def sample_triangle_pointset_bytes():
    """Fournit un échantillon de données binaires représentant un PointSet avec 3 points formant un triangle."""
    # 3 points: (0,0), (1,0), (0,1)
    b = struct.pack('<I', 3)
    b += struct.pack('<dd', 0.0, 0.0)
    b += struct.pack('<dd', 1.0, 0.0)
    b += struct.pack('<dd', 0.0, 1.0)
    return b
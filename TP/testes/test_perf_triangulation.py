import pytest
import time
import random

# triangulation = pytest.importorskip("triangulator.triangulation", reason="triangulator.triangulation introuvable")
# triangulate = getattr(triangulation, "triangulate", None)
# if triangulate is None:
#     pytest.skip("fonction triangulate introuvable", allow_module_level=True)

@pytest.mark.perf
def test_triangulation_time_small():
    random.seed(0)
    pts = [(random.random()*100.0, random.random()*100.0) for _ in range(1000)]
    start = time.perf_counter()
    triangulate(pts)
    elapsed = time.perf_counter() - start
    # Pas de valeur absolue imposée : limiter les régressions locales.
    # Ici on exige que l'opération prenne moins de 5 secondes sur une machine raisonnable.
    assert elapsed < 5.0, f"Triangulation lente: {elapsed:.2f}s"

@pytest.mark.perf
def test_triangulation_time_medium():
    random.seed(1)
    pts = [(random.random()*100.0, random.random()*100.0) for _ in range(10000)]
    start = time.perf_counter()
    triangulate(pts)
    elapsed = time.perf_counter() - start
    # Tolérance large, ajustez selon votre cible
    assert elapsed < 30.0, f"Triangulation medium lente: {elapsed:.2f}s"
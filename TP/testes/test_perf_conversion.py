"""
Tests de performance pour la conversion binaire <-> représentation interne
(PointSet et Triangles).

- Mesure le temps de sérialisation (serialize_pointset / serialize_triangles)
  et désérialisation (deserialize_pointset / deserialize_triangles).
- Paramétré sur plusieurs tailles de jeux de données.
- Marqué pytest.mark.perf pour permettre d'exclure ces tests dans une exécution
  rapide (pytest -m "not perf").
- Les seuils de performance sont volontairement permissifs ; ajustez-les selon
  votre machine/CI ou fournissez la variable d'environnement PERF_THRESHOLDS
  au format JSON pour surcharger.
"""

import os
import time
import random
import json
import math
import pytest

serializers = pytest.importorskip(
    "triangulator.serializers",
    reason="Module triangulator.serializers introuvable (nécessaire pour ces tests)"
)

serialize_pointset = getattr(serializers, "serialize_pointset", None)
deserialize_pointset = getattr(serializers, "deserialize_pointset", None)
serialize_triangles = getattr(serializers, "serialize_triangles", None)
deserialize_triangles = getattr(serializers, "deserialize_triangles", None)

if not (serialize_pointset and deserialize_pointset and serialize_triangles and deserialize_triangles):
    pytest.skip("Fonctions de sérialisation/désérialisation attendues introuvables", allow_module_level=True)


def generate_random_points(n, seed=0):
    rnd = random.Random(seed)
    return [(rnd.random() * 1000.0, rnd.random() * 1000.0) for _ in range(n)]


def generate_grid_triangles(nx, ny):
    """
    Génère une grille de points nx * ny et construit une liste de triangles
    couvrant la grille (2 triangles par cellule), ainsi que la liste des points.
    Retour: points, triangles
    """
    points = []
    for j in range(ny):
        for i in range(nx):
            points.append((float(i), float(j)))
    def idx(i, j): return j * nx + i
    triangles = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            # carré (i,j), (i+1,j), (i,j+1), (i+1,j+1)
            a = idx(i, j)
            b = idx(i+1, j)
            c = idx(i, j+1)
            d = idx(i+1, j+1)
            # deux triangles (a,b,c) et (b,d,c)
            triangles.append((a, b, c))
            triangles.append((b, d, c))
    return points, triangles


# Seuils par défaut (en secondes). Très permissifs — adaptez selon votre CI.
DEFAULT_THRESHOLDS = {
    "pointset": {
        1000: 1.0,
        5000: 3.0,
        20000: 12.0,
    },
    "triangles": {
        # for grid sizes: (nx,ny) roughly giving similar #points
        (50, 40): 2.0,   # ~2000 points -> ~ (49*39*2)=3822 triangles
        (100, 100): 15.0, # 10k points -> ~2*(99*99)=19602 triangles
    }
}

# Allow override with env var PERF_THRESHOLDS containing a JSON dict
env_thresh = os.getenv("PERF_THRESHOLDS")
if env_thresh:
    try:
        user_thresh = json.loads(env_thresh)
        # merge shallowly with defaults
        for k in ("pointset", "triangles"):
            if k in user_thresh:
                DEFAULT_THRESHOLDS[k].update(user_thresh[k])
    except Exception:
        # ignore parse errors and keep defaults
        pass


@pytest.mark.perf
@pytest.mark.parametrize("n_points", [1000, 5000, 20000])
def test_pointset_serialize_deserialize_perf(n_points):
    """
    Mesure le temps pour serializer puis désérialiser un PointSet de taille n_points.
    Vérifie que la sérialisation/désérialisation complète reste en dessous d'un seuil.
    """
    pts = generate_random_points(n_points, seed=12345)
    # warmup
    b = serialize_pointset(pts)
    _ = deserialize_pointset(b)

    # mesurer sérialisation
    iters = 3
    ser_times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        b = serialize_pointset(pts)
        t1 = time.perf_counter()
        ser_times.append(t1 - t0)
    ser_avg = sum(ser_times) / len(ser_times)

    # mesurer désérialisation
    deser_times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        pts2 = deserialize_pointset(b)
        t1 = time.perf_counter()
        deser_times.append(t1 - t0)
    deser_avg = sum(deser_times) / len(deser_times)

    total = ser_avg + deser_avg

    # vérification d'intégrité rapide : taille et quelques valeurs
    assert len(pts2) == len(pts)
    if len(pts) > 0:
        # comparer quelques éléments avec tolérance float
        for i in (0, len(pts)//2, len(pts)-1):
            assert math.isclose(pts[i][0], pts2[i][0], rel_tol=1e-6, abs_tol=1e-6)
            assert math.isclose(pts[i][1], pts2[i][1], rel_tol=1e-6, abs_tol=1e-6)

    # Reporter les temps (utile pour logs CI)
    print(f"[perf] pointset n={n_points} ser_avg={ser_avg:.4f}s deser_avg={deser_avg:.4f}s total={total:.4f}s")

    # Assertion optionnelle selon seuil
    threshold = DEFAULT_THRESHOLDS["pointset"].get(n_points)
    if threshold is not None:
        assert total <= threshold, f"Conversion PointSet lente pour n={n_points}: {total:.2f}s > {threshold:.2f}s"


@pytest.mark.perf
@pytest.mark.parametrize("grid_size", [(50, 40), (100, 100)])
def test_triangles_serialize_deserialize_perf(grid_size):
    """
    Mesure le temps pour serializer puis désérialiser la structure Triangles
    (points + liste de triangles) construite à partir d'une grille.
    """
    nx, ny = grid_size
    points, triangles = generate_grid_triangles(nx, ny)

    # warmup
    b = serialize_triangles(points, triangles)
    _ = deserialize_triangles(b)

    # mesurer sérialisation
    iters = 3
    ser_times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        b = serialize_triangles(points, triangles)
        t1 = time.perf_counter()
        ser_times.append(t1 - t0)
    ser_avg = sum(ser_times) / len(ser_times)

    # mesurer désérialisation
    deser_times = []
    for _ in range(iters):
        t0 = time.perf_counter()
        pts2, tris2 = deserialize_triangles(b)
        t1 = time.perf_counter()
        deser_times.append(t1 - t0)
    deser_avg = sum(deser_times) / len(deser_times)

    total = ser_avg + deser_avg

    # vérifications d'intégrité rapides
    assert len(pts2) == len(points)
    assert len(tris2) == len(triangles)
    # vérifier quelques indices
    if len(triangles) > 0:
        for idx in (0, len(triangles)//2, len(triangles)-1):
            assert tris2[idx] == triangles[idx]

    print(f"[perf] triangles grid={nx}x{ny} points={len(points)} triangles={len(triangles)} ser_avg={ser_avg:.4f}s deser_avg={deser_avg:.4f}s total={total:.4f}s")

    threshold = DEFAULT_THRESHOLDS["triangles"].get((nx, ny))
    if threshold is not None:
        assert total <= threshold, f"Conversion Triangles lente pour grid {nx}x{ny}: {total:.2f}s > {threshold:.2f}s"
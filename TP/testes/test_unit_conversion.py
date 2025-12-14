"""Tests unitaires pour la conversion binaire PointSet et Triangles."""
import struct
from unittest.mock import Mock

import pytest

from TP.Code.serializers import bytes_to_pointset, triangles_to_bytes

# tester si le nombre de point correspond au nombre de point en bytes

def test_bytes_to_pointset():
    """Test la conversion binaire d'un set de points avec plusieurs points."""
    nbr_points = struct.pack('<I', 3)
    point1 = struct.pack('<dd', 1.0, 2.0)
    point2 = struct.pack('<dd', -3.5, 0.25)
    point3 = struct.pack('<dd', 10.0, -1.0)
    point_bytes = nbr_points + point1 + point2 + point3
    assert bytes_to_pointset(point_bytes) == {"nbr_point": 3, "points": [(1.0, 2.0), (-3.5, 0.25), (10.0, -1.0)]}

def test_bytes_to_pointset_negative_points():
    """Test la conversion binaire d'un set de points avec des coordonnées négatives."""
    nbr_points = struct.pack('<I', 2)
    point1 = struct.pack('<dd', -1.0, -2.0)
    point2 = struct.pack('<dd', -3.5, -0.25)
    point_bytes = nbr_points + point1 + point2
    assert bytes_to_pointset(point_bytes) == {"nbr_point": 2, "points": [(-1.0, -2.0), (-3.5, -0.25)]}

def test_bytes_to_pointset_grand_points():
    """Test la conversion binaire d'un set de points avec des grandes coordonnées."""
    nbr_points = struct.pack('<I', 2)
    point1 = struct.pack('<dd', 1e9, -1e9)
    point2 = struct.pack('<dd', -1e10, 1e10)
    point_bytes = nbr_points + point1 + point2
    assert bytes_to_pointset(point_bytes) == {"nbr_point": 2, "points": [(1e9, -1e9), (-1e10, 1e10)]}

def test_bytes_to_pointset_petit_points():
    """Test la conversion binaire d'un set de points avec des petites coordonnées."""
    nbr_points = struct.pack('<I', 2)
    point1 = struct.pack('<dd', 1e-9, -1e-9)
    point2 = struct.pack('<dd', -1e-10, 1e-10)
    point_bytes = nbr_points + point1 + point2
    assert bytes_to_pointset(point_bytes) == {"nbr_point": 2, "points": [(1e-9, -1e-9), (-1e-10, 1e-10)]}

def test_bytes_to_pointset_insufficient_bytes():
    """Test la gestion des données binaires insuffisantes pour le nombre de points spécifié."""
    nbr_points = struct.pack('<I', 2)
    point1 = struct.pack('<dd', 1.0, 2.0)
    point_bytes = nbr_points + point1  
    with pytest.raises(ValueError, match="Insufficient bytes for the specified number of points"):
        bytes_to_pointset(point_bytes)

def test_bytes_to_pointset_empty():
    """Test la conversion d'un set de points vide (0 points)."""
    nbr_points = struct.pack('<I', 0)
    # Pas de données de points attendues
    assert bytes_to_pointset(nbr_points) == {"nbr_point": 0, "points": []}

def test_bytes_to_pointset_extra_data_ignored():
    """Vérifie que les données excédentaires après les points définis sont ignorées (ou gérées)."""
    nbr_points = struct.pack('<I', 1)
    point1 = struct.pack('<dd', 5.5, 5.5)
    extra_garbage = b'\xDE\xAD\xBE\xEF' # Données en trop à la fin
    
    point_bytes = nbr_points + point1 + extra_garbage
    
    # La fonction doit lire 1 point et s'arrêter, ignorant le reste
    result = bytes_to_pointset(point_bytes)
    assert result["nbr_point"] == 1
    assert result["points"] == [(5.5, 5.5)]

def test_triangles_to_bytes():
    """Test la sérialisation binaire de points et triangles."""
    triangles= Mock()
    point_set = Mock()
    point_set.get_points.return_value = [(0.0,0.0), (1.0,0.0), (0.0,1.0), (1.0,1.0)]
    point_set.n_points.return_value = 4
    triangles.n_triangles.return_value = 2
    triangles.get_triangles.return_value = [ (0,1,2), (1,2,3) ]

    n_points = struct.pack('<I', 4) 
    point1 = struct.pack('<dd', 0.0, 0.0)
    point2 = struct.pack('<dd', 1.0, 0.0)
    point3 = struct.pack('<dd', 0.0, 1.0)
    point4 = struct.pack('<dd', 1.0, 1.0) 
    nbr_triangles = struct.pack('<I', 2)
    triangle1 = struct.pack('<III', 0, 1, 2)
    triangle2 = struct.pack('<III', 1, 2, 3)
    expected_bytes = n_points + point1 + point2 + point3 + point4 + nbr_triangles + triangle1 + triangle2
    assert triangles_to_bytes(triangles.n_triangles(), triangles.get_triangles(),point_set.n_points(),point_set.get_points()) == expected_bytes


def test_triangles_to_bytes_empty():
    """Test la sérialisation quand il n'y a aucun point ni triangle."""
    triangles = Mock()
    point_set = Mock()
    
    point_set.get_points.return_value = []
    point_set.n_points.return_value = 0
    triangles.n_triangles.return_value = 0
    triangles.get_triangles.return_value = []
    with pytest.raises(Exception, match="No triangles to serialize"):
        triangles_to_bytes(triangles.n_triangles(), triangles.get_triangles(),point_set.n_points(),point_set.get_points())
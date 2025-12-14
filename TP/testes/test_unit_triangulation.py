"""Tests unitaires pour la triangulation."""

from unittest.mock import Mock

import pytest

from TP.Code.triangulation import triangulate


def test_cas_nominal():
    """Test de triangulation simple avec 3 points formant un triangle."""
    t= triangulate([(0.0,0.0), (1.0,0.0), (0.0,1.0)])

    assert len(t) == 1
    print(t)
    assert t== [ (0,1,2) ]

# tester le cas ou on a plusieru points dans le PointSet
def test_cas_simple():
    """Test de triangulation avec 4 points formant un carré."""
    point_set= Mock()
    point_set.get_points.return_value= [(0.0,0.0), (1.0,0.0), (0.0,1.0), (1.0,1.0)]
    point_set.n_points.return_value= 4
    t= triangulate(point_set.get_points())
    assert len(t) == 2
    solutions = [
        {(0,1,2), (1,2,3)},
        {(0,1,3), (0,2,3)}
    ]
    assert set(t) in solutions

def test_cas_simple2():
    """Test de triangulation avec 7 points formant une configuration simple."""
    point_set= Mock()
    point_set.get_points.return_value= [(0.0,0.0), (2.0,0.0), (1.0,1.0), (0.0,2.0), (2.0,2.0), (3.0,1.0), (1.0,3.0)]
    t= triangulate(point_set.get_points())
    assert len(t) == 6
    solution = [{
        (0,1,2),
        (0,2,3),
        (1,2,4),
        (1,4,5),
        (2,3,4),
        (3,4,6)
    }]
    assert set(t) in solution

def test_coordonnees_negatives():
    """Test de triangulation avec des coordonnées négatives."""
    points = [(-1,-1), (1,-1), (-1,1), (1,1)]
    t = triangulate(points)
    assert len(t) == 2
    solutions = [
        {(0,1,2), (1,2,3)},
        {(0,1,3), (0,2,3)}
    ]
    assert set(t) in solutions


def test_grandes_coordonnees():
    """Test de triangulation avec des grandes coordonnées."""
    points = [
        (1e9, 1e9),
        (1e9+1, 1e9),
        (1e9, 1e9+1),
        (1e9+1, 1e9+1)
    ]
    t = triangulate(points)
    assert len(t) == 2
    solutions = [
        {(0,1,2), (1,2,3)},
        {(0,1,3), (0,2,3)}
    ]
    assert set(t) in solutions

def test_petites_coordonnees():
    """Test de triangulation avec des petites coordonnées."""
    points = [
        (1e-9, 1e-9),
        ((1e-9)+1, 1e-9),
        (1e-9, (1e-9)+1),
        ((1e-9)+1, (1e-9)+1)
    ]
    t = triangulate(points)
    assert len(t) == 2
    solutions = [
        {(0,1,2), (1,2,3)},
        {(0,1,3), (0,2,3)}
    ]
    assert set(t) in solutions



def test_cas_vide():
    """Test de triangulation avec un PointSet vide."""
    point_set= Mock()
    point_set.get_points.return_value= []
    point_set.n_points.return_value= 0

    with pytest.raises(Exception, match="Insufficient points to form a triangle"):
        triangulate(point_set.get_points())
            

def test_cas_limite():
    """Test de triangulation avec un PointSet ayant seulement 2 points."""
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (1,0)]
    point_set.n_points.return_value= 2

    with pytest.raises(Exception, match="Insufficient points to form a triangle"):
        triangulate(point_set.get_points())

def test_cas_point_dupliques():
    """Test de triangulation avec des points dupliqués."""
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (1,0), (0,1), (0,0)]
    point_set.n_points.return_value= 4

    with pytest.raises(Exception, match="Duplicate points found"):
        triangulate(point_set.get_points())

def test_cas_point_colineaires():
    """Test de triangulation avec des points colinéaires."""
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (1,1), (2,2), (3,3)]
    point_set.n_points.return_value= 4

    with pytest.raises(Exception, match="All points are colinear"):
        triangulate(point_set.get_points())

import pytest
from unittest.mock import Mock


def test_cas_nominal():
    
    t= triangulate([(0.0,0.0), (1.0,0.0), (0.0,1.0)])

    assert len(t) == 3
    assert t== [ (0,1,2) ]

# tester le cas ou on a plusieru points dans le PointSet
def test_cas_simple():
    point_set= Mock()
    point_set.get_points.return_value= [(0.0,0.0), (1.0,0.0), (0.0,1.0), (1.0,1.0)]
    point_set.n_points.return_value= 4
    t= triangulate(point_set.get_points())
    assert len(t) == 2
    assert t == [ (0,1,2), (1,2,3) ] 

def test_cas_simple2():
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (2,0), (1,1), (0,2), (2,2), (3,1), (1,3)]
    t= triangulate(point_set.get_points())
    assert t.get_triangles() == [ (0,1,2), (0,2,3), (1,4,2), (3,2,6), (1,5,4), (5,6,4) ]  # Exemple attendu
    assert t.n_triangles() == 6

def test_cas_vide():
    point_set= Mock()
    point_set.get_points.return_value= []
    point_set.n_points.return_value= 0

    with pytest.raises(Exception, match="Insufficient points to form a triangle"):
        triangulate(point_set.get_points())
            

def test_cas_limite():
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (1,0)]
    point_set.n_points.return_value= 2

    with pytest.raises(Exception, match="Insufficient points to form a triangle"):
        triangulate(point_set.get_points())

def test_cas_point_dupliques():
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (1,0), (0,1), (0,0)]
    point_set.n_points.return_value= 4

    with pytest.raises(Exception, match="Duplicate points found"):
        triangulate(point_set.get_points())

def test_cas_point_colineaires():
    point_set= Mock()
    point_set.get_points.return_value= [(0,0), (1,1), (2,2), (3,3), (1,0)]
    point_set.n_points.return_value= 4

    with pytest.raises(Exception, match="All points are colinear"):
        triangulate(point_set.get_points())
        

from unittest.mock import Mock
from unittest import mock
# tester si le nombre de point correspond au nombre de point en bytes

def test_bytes_to_pointset_points():
    point_bytes = b'\x03\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x00\x40\x00\x00\x60\xC0\x00\x00\x80\x3E\x00\x00\x20\x41\x00\x00\x80\xBF'
    assert bytes_to_pointset_nb_points(point_bytes) == {"nbr_point": 3, "points": [(1.0, 2.0), (-3.5, 0.25), (10.0, -1.0)]}

def test_bytes_to_pointset_insufficient_bytes():
    point_bytes = b'\x02\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x00'  # Incomplet
    with pytest.raises(ValueError, match="Insufficient bytes for the specified number of points"):
        bytes_to_pointset_nb_points(point_bytes)
    

def test_triangles_to_bytes():
    # pointsetID = 1
    # triangle = Triangulator() # un mock de triangulator
    # # triangle.get_nbr_triangles.return_value = 3
    # # triangle.get_points.return_value =  [(0.0,0.0), (1.0,0.0), (0.0,1.0), (1.0,1.0)]
    # # triangle.get_triangles.return_value = [ (0,1,2), (1,2,3) ]
    # with mock.patch.object(Triangulator, 'n_triangles', return_value=3),
    #         mock.patch.object(Triangulator, 'get_points', return_value=[(0.0,0.0), (1.0,0.0), (0.0,1.0), (1.0,1.0)]),
    #         mock.patch.object(Triangulator, 'get_triangles', return_value=[ (0,1,2), (1,2,3) ]) :
    triangles= Mock()
    point_set = Mock()
    point_set.get_points.return_value = [(0.0,0.0), (1.0,0.0), (0.0,1.0), (1.0,1.0)]
    point_set.n_points.return_value = 4
    triangles.n_triangles.return_value = 2
    triangles.get_triangles.return_value = [ (0,1,2), (1,2,3) ]

    expected_bytes = b'\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x01\x02\x00\x00\x03\x00\x00'
    assert triangles_to_bytes(triangles.n_triangles, triangles.get_triangles,point_set.n_points,point_set.get_points) == expected_bytes

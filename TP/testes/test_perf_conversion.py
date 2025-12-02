import os
import time
import random
import json
import math
import pytest
import struct

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




@pytest.mark.perf
def test_bytes_to_pointset_time_small():

    pts = generate_random_points(1000, seed=12345)

    point_bytes = struct.pack('I', len(pts))
    for x,y in pts:
        point = struct.pack('<dd', x,y)
        point_bytes = point_bytes + point

        
    # mesurer désérialisation
    t0 = time.perf_counter()
    pts2 = bytes_to_pointset(point_bytes)
    t1 = time.perf_counter()
    deser_times = (t1 - t0)
    
    assert deser_times < 1.0

@pytest.mark.perf
def test_bytes_to_pointset_time_meduim():

    pts = generate_random_points(5000, seed=12345)

    point_bytes = struct.pack('I', len(pts))
    for x,y in pts:
        point = struct.pack('<dd', x,y)
        point_bytes = point_bytes + point

        
    # mesurer désérialisation
    t0 = time.perf_counter()
    pts2 = bytes_to_pointset(point_bytes)
    t1 = time.perf_counter()
    deser_times = (t1 - t0)
    
    assert deser_times < 3.0

@pytest.mark.perf
def test_bytes_to_pointset_time_large():

    pts = generate_random_points(20000, seed=12345)

    point_bytes = struct.pack('I', len(pts))
    for x,y in pts:
        point = struct.pack('<dd', x,y)
        point_bytes = point_bytes + point

        
    # mesurer désérialisation
    t0 = time.perf_counter()
    pts2 = bytes_to_pointset(point_bytes)
    t1 = time.perf_counter()
    deser_times = (t1 - t0)
    
    assert deser_times < 12.0

@pytest.mark.perf
def test_triangles_to_bytes_small():
    points, triangles_list = generate_grid_triangles(50, 40)
    n_triangles = len(triangles_list)
    n_points = len(points)
    
    
    t0 = time.perf_counter()
    b = triangles_to_bytes(n_triangles,triangles_list,n_points,points)
    t1 = time.perf_counter()
    ser_times = (t1 - t0)

    assert ser_times < 2.0

@pytest.mark.perf
def test_triangles_to_bytes_large():
    points, triangles_list = generate_grid_triangles(100, 100)
    n_triangles = len(triangles_list)
    n_points = len(points)
    
    t0 = time.perf_counter()
    b = serialize_triangles(points, triangles)
    t1 = time.perf_counter()
    ser_times = (t1 - t0)

    assert ser_times < 15.0

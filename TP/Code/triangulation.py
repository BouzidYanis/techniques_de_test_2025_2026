""""Module de triangulation de Delaunay en pur Python."""
# La classe TriangulationResult a été supprimée car inutile désormais.

# def _dist_sq(p1, p2):
#     return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def _is_collinear(p1, p2, p3):
    """Vérifie si 3 points sont colinéaires (produit vectoriel nul)."""
    return abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])) < 1e-9

def _circumcircle_contains(tri, p, points):
    """Vérifie si le point p est dans le cercle circonscrit du triangle tri.
    
    tri: tuple d'indices (a, b, c)
    p: tuple de coordonnées (x, y)
    points: liste de tous les points (coordonnées)
    """
    p1 = points[tri[0]]
    p2 = points[tri[1]]
    p3 = points[tri[2]]

    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))

    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    
    # Rayon au carré
    r_sq = (ux - ax)**2 + (uy - ay)**2
    # Distance au carré du point p au centre
    d_sq = (ux - p[0])**2 + (uy - p[1])**2

    return d_sq < r_sq - 1e-9 # Epsilon pour la précision flottante

def triangulate(points):
    """Réalise une triangulation de Delaunay (Bowyer-Watson) (https://fr.wikipedia.org/wiki/Algorithme_de_Bowyer-Watson) en pur Python.

    Retourne une liste de tuples (p1, p2, p3) représentant les indices des points.
    """
    n = len(points)
    if not points or n < 3:
        raise ValueError("Insufficient points to form a triangle")

    # 1. Vérification des doublons
    if len(set(points)) != n:
        raise ValueError("Duplicate points found")

    # 2. Vérification de la colinéarité globale
    p0 = points[0]
    p1 = points[1]
    all_collinear = True
    for i in range(2, n):
        if not _is_collinear(p0, p1, points[i]):
            all_collinear = False
            break
    
    if all_collinear:
        raise ValueError("All points are colinear")

    # 3. Algorithme de Bowyer-Watson
    
    # Création d'un super-triangle qui englobe tous les points
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    
    # Sommets du super-triangle (indices n, n+1, n+2)

    st_scale = 1e6 * max(1.0, delta_max)
    p_st1 = (mid_x - 2.0 * st_scale, mid_y - st_scale)
    p_st2 = (mid_x,               mid_y + 2.0 * st_scale)
    p_st3 = (mid_x + 2.0 * st_scale, mid_y - st_scale)
    
    temp_points = points + [p_st1, p_st2, p_st3]
    triangles = [(n, n+1, n+2)]
    
    for i in range(n):
        point = points[i]
        bad_triangles = []
        
        for tri in triangles:
            if _circumcircle_contains(tri, point, temp_points):
                bad_triangles.append(tri)
        
        polygon = []
        for tri in bad_triangles:
            edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
            for edge in edges:
                shared = False
                for other_tri in bad_triangles:
                    if other_tri == tri:
                        continue
                    if (edge[0] in other_tri and edge[1] in other_tri):
                         shared = True
                         break
                if not shared:
                    polygon.append(edge)
        
        for tri in bad_triangles:
            triangles.remove(tri)
            
        for edge in polygon:
            triangles.append((edge[0], edge[1], i))
            
    # 4. Nettoyage
    final_triangles = []
    for tri in triangles:
        if tri[0] < n and tri[1] < n and tri[2] < n:
            final_triangles.append(tuple(sorted(tri)))
            
    return final_triangles
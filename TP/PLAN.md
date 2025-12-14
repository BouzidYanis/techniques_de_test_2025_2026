
## 1. Tests Unitaires de la triangulation
### Objectif
Vérifier que l’algorithme de triangulation produit des résultats corrects pour différents ensembles de points.
### Méthode
<!-- #### 1.1. Tests de la logique de triangulation -->
- **Cas simple :** Vérifier que les triangles retounés sont correctes après lui avoir donner un `PointSet` contenant plus que 3 points (pas de chauvechement, couverture totales des points).
- **Cas nominal :** Vérifier que la triangulation d'un `PointSet` contenant 3 points retourne 1 triangle.
- **Cas avec coordonnées négatives :** Vérifier que la triangulation d'un `PointSet` avec des coordonnées négatives fonctionne correctement.
- **Cas avec des grandes coordonnées :** Vérifier que la triangulation d'un `PointSet` avec des coordonnées très grandes (ex : 1e9) fonctionne correctement.
- **Cas avec des petites coordonnées :** Vérifier que la triangulation d'un `PointSet` avec des coordonnées très petites (ex : 1e-9) fonctionne correctement.
- **Testes d'erreurs :** 
- - **Cas limite :** Vérifier que la triangulation d'un `PointSet` contenant moins de 3 points retourne une erreur avec le message "nombre de points n'est pas suffisant".
- - **Cas vide :** Vérifier que la triangulation d'un `PointSet` vide retourne une erreur avec le message "PointSet vide".
- - **Cas point dupliqués :** Vérifier que la triangulation d'un `PointSet` qui contient des points duppliqués retourne une erreur "il y a des points duppliqués".
- - **Cas Points colinéaires uniquement :** Vérifier que la triangulation d'un `PointSet` contenant uniquement des points colinéaires retourne une erreur "points colinéaires uniquement".

---

## 2. Tests d'integration API
### Objectif
Assurer que l’API HTTP du Triangulator respecte la spécification OpenAPI et fonctionne de bout en bout.
### Méthodes
- Simuler l’appel API pour demander une triangulation avec un PointSetID valide.
- Mock ou stub pour simuler les réponses du PointSetManager.
- Vérifier les réponses correctes (status HTTP, corps de réponse binaire conforme).
- Tests d’erreurs : PointSetID non existant, erreurs réseau, données malformées.

---
## 3. Tests de format et conversion
### Objectif
Valider la conversion entre les représentations binaires et internes des structures PointSet et Triangles.
### Méthodes 
- Tests de sérialisation/désérialisation pour plusieurs jeux de points.
- Vérification que la conversion binaire → interne → binaire est une opération sans perte.
- Gestion des formats invalides ou corrompus.

---
## 4. Tests de Performance
### Objectif
Mesurer les performances de la triangulation et des conversions binaires sous différentes tailles de données.
### Méthodes
- Mesurer le temps de calcul de la triangulation pour des `PointSet` de différentes tailles (petit, moyen, grand).
- Mesurer le temps de conversion entre les représentations binaires et internes pour des `PointSet` et `Triangles` de différentes tailles.
- Vérifier que le temps de calcul reste dans des limites acceptables pour des ensembles de points réalistes.

---

## 5. Tests de Qualité
### Objectif
Maintenir un code lisible, bien documenté et conforme aux normes définies.
### Méthodes
#### 5.1. Couverture de code
- Tests assurant la couverture maximale du code via `coverage`.

#### 5.2. Qualité de code
- Utiliser `ruff` pour s'assurer que le code respecte les standards de qualité définis.

#### 5.3. Documentation
- Vérifier que la documentation générée avec `pdoc3` est complète et conforme.

---

## 6. Tests de robustesse et gestion d’erreurs
### Objectif
Assurer que le composant gère proprement les entrées invalides et les erreurs de communication.
### Méthodes
- Tests d’API avec données invalides ou absentes.
- Simulations d’erreurs de réseau lors de la récupération du PointSet depuis le PointSetManager.
- Tests sur gestion d’exceptions et messages d’erreur clairs.
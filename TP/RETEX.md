# RETEX – Retour d’expérience sur le projet de Triangulation

## Introduction

Ce document présente mon retour d’expérience (RETEX) sur le projet de **Triangulation de Delaunay** réalisé dans le cadre du TP de *Techniques de Test*. L’objectif du projet était de concevoir et tester un micro-service de triangulation, en adoptant une démarche *test-first*, avec une attention particulière portée à la qualité, à la pertinence des tests et à la robustesse de l’implémentation.

---

## Ce qui a bien fonctionné

Plusieurs points positifs peuvent être relevés durant ce projet.

Tout d'abord, la mise en place de **tests unitaires dès le début** a été bénéfique. Elle a permis d’identifier rapidement des erreurs de logique et des cas limites, notamment les ensembles de points insuffisants, colinéaires ou contenant des doublons.

L’utilisation de **pytest** s’est avérée efficace pour automatiser les tests et obtenir des rapports clairs sur la couverture de code.

L'utilisation de **mocks** pour simuler les interactions avec le PointSetManager dans les tests d’intégration API a permis de se concentrer sur le comportement du Triangulator sans dépendre d’un service externe.

Enfin, le projet a permis de bien appliquer les outils demandés : pytest pour les tests, ruff pour la qualité de code, et une organisation claire des fichiers. La séparation entre tests unitaires, tests de performance a facilité le débogage.

---

## Difficultés rencontrées

La principale difficulté a concerné les **cas géométriques dégénérés**. En particulier, la gestion des points cocycliques (par exemple les sommets d’un carré) a posé problème, car la triangulation de Delaunay n’est pas unique dans ces cas. Certains tests initiaux supposaient à tort une solution unique, ce qui a nécessité une révision de la stratégie de test.

Un autre point délicat a été la **stabilité numérique**. Les tests utilisant de grandes coordonnées ont révélé des limites dans les comparaisons flottantes, notamment lors du calcul des cercles circonscrits. Le choix d’un epsilon absolu s’est avéré insuffisant dans certains cas.

Les tests de performance ont également été plus complexes que prévu, notamment pour garantir des temps de calcul raisonnables sur de grands ensembles de points.

Enfin, la rédaction de tests d’intégration pour l’API HTTP a été plus complexe que prévu, notamment en raison de la nécessité de simuler les interactions avec le PointSetManager et la couverture de code m'a revelée des lacunes dans les tests unitaires initiaux.

---

## Ce que je ferais différemment avec le recul

Avec le recul, plusieurs améliorations seraient envisageables.

Je commencerais par définir dès le départ des **tests basés sur des propriétés mathématiques** (propriété de Delaunay) plutôt que sur des résultats exacts. Cela aurait évité de devoir corriger certains tests supposant une triangulation unique.

Je porterais également une attention plus précoce aux **problèmes numériques**, par exemple en recentrant les points avant les calculs ou en utilisant des epsilons relatifs plutôt qu’absolus.

Je prendrais en compte plus tôt les aspects de performance, notamment la complexité de l’algorithme et le coût des calculs géométriques.

Enfin, je consacrerais plus de temps en amont à l’étude des cas limites théoriques afin d’anticiper les difficultés rencontrées lors de l’implémentation.

---

## Analyse du plan initial

Le plan initial reposait sur une démarche *test-first*, consistant à définir et écrire les tests avant l’implémentation de l’algorithme de triangulation. Cette approche a permis de clarifier dès le départ le comportement attendu du composant et de structurer le développement autour des cas à valider.

En pratique, ce plan s’est révélé pertinent, mais il sous-estimait la complexité de certains aspects, notamment les cas géométriques dégénérés et les problèmes numériques. La conception des tests a nécessité autant de réflexion que l’implémentation elle-même, et les tests ont naturellement évolué au fil du projet, ce qui correspond pleinement à l’esprit de l’exercice.

---

## Apports et apprentissages

Ce projet a été très formateur. Il a permis de mieux comprendre le rôle et la complémentarité des **tests unitaires**, des **tests d’intégration** et des **tests de performance**, ainsi que l’utilisation des **mocks**, dans le contexte du développement logiciel.

Sur le plan méthodologique, il a renforcé l’importance de concevoir des **tests unitaires pertinents**, et non uniquement nombreux, en mettant en évidence la différence entre la **couverture de code** et la **qualité réelle des tests**.

Enfin, ce projet a souligné l’intérêt de documenter et de structurer correctement le code afin d’en faciliter la maintenance, l’évolution et la compréhension à long terme.


---

## Conclusion

En conclusion, ce projet a été exigeant mais très enrichissant sur le plan méthodologique. Il a permis de développer une approche plus rigoureuse de la programmation orientée tests, en mettant l’accent sur la conception, l’exécution et l’évolution des tests tout au long du cycle de développement.

Les difficultés rencontrées ont mis en évidence l’importance de tests bien pensés, capables de couvrir des cas limites, de révéler des comportements inattendus et de guider les choix d’implémentation. Ce projet a ainsi renforcé la compréhension du rôle central des tests automatisés dans l’amélioration de la fiabilité, de la robustesse et de la maintenabilité d’un logiciel.

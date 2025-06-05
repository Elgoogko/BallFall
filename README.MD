# Halo Ball Game

Halo Ball Game est une démonstration interactive réalisée avec Pygame. Une balle est projetée vers le bas et tente de franchir une série d'anneaux (ou "halos") circulaires en rotation, chacun comportant une ouverture. L'objectif est d'optimiser la physique pour que la balle puisse traverser les anneaux sans que la difficulté ne croisse de façon déséquilibrée.

## Fonctionnalités

* Balle avec simulation de gravité et rebond contre les cercles
* Anneaux circulaires tournant avec des vitesses légèrement différentes pour éviter les alignements parfaits
* Trainée visuelle derrière la balle pour accentuer son mouvement
* Gestion dynamique des anneaux pour un effet de défilement

## Objectifs de gameplay

* Empêcher l'accélération excessive de la balle lors de la progression
* Maintenir une vitesse visuelle constante des anneaux visibles
* Introduire de l'aléatoire subtil pour éviter des trajectoires parfaites et ajouter de la variété

## Fichiers principaux

* `main.py` : contient la logique principale du jeu (affichage, créations des objets)
* `BallClass.py` : Classe balle avec ses attributs et fonctions
* `HaloClass.py` : Classe anneau avec ses attributs et fonctions
* `README.md` : présente le projet et ses objectifs

## Prérequis

* Python 3.10+
* Pygame

Installation des dépendances :

```bash
pip install pygame
```

## Lancement du jeu

```bash
python main.py
```

## Idées d'amélioration

* Ajouter un compteur de score ou de progression
* Implémenter une génération dynamique des anneaux plutôt qu'une liste pré-générée
* Ajout de sons et d'effets visuels pour les rebonds et le passage d'anneau

## Licence

Ce projet est distribué sous licence MIT.

## Auteur

Projet développé dans le cadre d'une expérimentation personnelle sur la biblothèque Pygame et dans le cadre d'un projet de re création de videos virales sur Tik Tok.

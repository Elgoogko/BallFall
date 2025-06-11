# Halo Ball Game

Halo Ball Game est une démonstration interactive réalisée avec Pygame. Une balle est projetée vers le bas et tente de franchir une série d'anneaux (ou "halos") circulaires en rotation, chacun comportant une ouverture. L'objectif est d'optimiser la physique pour que la balle puisse traverser les anneaux sans que la difficulté ne croisse de façon déséquilibrée.

## Fonctionnalités

* Balle avec simulation de gravité et rebond contre les cercles
* Anneaux circulaires tournant 
* Trainée visuelle derrière la balle pour accentuer son mouvement
* Tous les paramètres sont de 
## Objectifs de gameplay

* Empêcher l'accélération excessive de la balle lors de la progression
* Maintenir une vitesse visuelle constante des anneaux visibles
* Introduire de l'aléatoire subtil pour éviter des trajectoires parfaites et ajouter de la variété

## Dossiers principaux

* `/music` : dossier contenant des musiques au format MIDI (à remplir vous même)
* `/sounds` : dossier contenant vos sons pour les balles
* `/test` : contient des jeux "Test" et les paramètres par défault
* `/scripts` : contient tous les scripts de l'application
* `/scripts/tools` : contient des scripts outils

## Scripts

* `BallFall.py` : Point d'entrtée de l'application, permet de lancer ou non l'installation et la mise à jour des bibliothèques
* `/scripts/BallClass.py` : Classe Balle, la balle qui rebondit dans les anneaux
* `/scripts/HaloClass.py` : Classe Halo, ce sont les anneaux qui sont affichées autour de la balle
* `/scripts/main.py`: jeu principal, initialise Pygamet et gère les évènements
* `/scripts/mainCLI.py` : Interface en ligne de commande
* `/scripts/MusicClass.py` : Gère la conversion du son MIDI en notes à jouer a chaque rebond d'une balle sur les anneaux
* `/scripts/tools/FileController.py` : Gère la sauvegarde et la restoration des sauvegardes
* `/scripts/tools/formatCLI.py` : Contient le formatage de l'interface en lignes de commandes (Couleurs, messages...)
* `/scripts/tools/UpdateInstall.py` : Installe OU met à jour les bibliothèques nécessaires au jeu
* `/scripts/tools/requirements.txt` : Listes des bibliothèques utilisées

## Prérequis

* Python 3.10+
* Pygame

## Bibliothèques audio
* Pydub
* pretty_midi
* numpy

### Déjà présent sur python
* inspect
* json

## Lancement du jeu

```bash
python BallFall.py
```
**Paramètres** : -p pour passer la vérification / l'installation des bibliothèques nécéssaires

## Licence

Ce projet est distribué sous licence MIT.

## Auteur

Projet développé dans le cadre d'une expérimentation personnelle sur la biblothèque Pygame et dans le cadre d'un projet de re création de videos virales sur Tik Tok.

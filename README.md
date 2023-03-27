# Guide d'utilisation du fichier main.py

Ce fichier contient une implémentation de plusieurs méthodes de vote pour déterminer un vainqueur à partir d'un fichier CSV.

## Prérequis

Python 3.7 ou supérieur doit être installé sur votre machine.
Les bibliothèques csv, numpy, pandas doivent être installées. Vous pouvez les installer en exécutant la commande suivante :

```
pip install csv numpy pandas
```

## Comment utiliser le code

Ouvrez un terminal ou une invite de commande dans le dossier contenant le fichier main.py.
Exécutez le fichier en exécutant la commande suivante :

```
python3 main.py
```

Puis suivez les instructions qui vous seront données par l'invite de commande. À savoir, choisir le profil de votes ainsi que la méthode pour analyser ce dernier.

## Méthodes implémentées

Les méthodes suivantes sont implémentées dans ce code :

* **Condorcet :** Détermine un gagnant suivant ce concept : "Si un choix est préféré à tout autre par une majorité ou une autre, alors ce choix doit être élu."
* **Borda :** Attribue des points à chaque candidat en fonction de son classement dans chaque vote, puis détermine le vainqueur en fonction du nombre total de points.
* **Rounds :** Réalise un ou deux tours de scrutin pour déterminer le vainqueur. Dans le premier tour, le candidat ayant obtenu le plus de premières places est déclaré vainqueur. Dans le deuxième tour, les deux candidats ayant obtenu le plus de voix au premier tour s'affrontent, et le candidat ayant obtenu le plus de voix est déclaré vainqueur.
* **Coombs :** Élimine le candidat ayant obtenu le plus de dernières places jusqu'à ce qu'un candidat obtienne plus de la moitié des voix.
* **Alternatif :** Élimine le candidat ayant obtenu le moins de premières places jusqu'à ce qu'un candidat obtienne plus de la moitié des voix.

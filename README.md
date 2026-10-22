# GUDLFT – Plateforme légère de réservation de compétitions

Preuve de concept (POC) d'une version allégée de la plateforme de réservation GUDLFT,
destinée aux organisateurs de compétitions locales et régionales.
Les secrétaires de clubs se connectent avec leur adresse e-mail et utilisent les points
de leur club pour réserver des places (1 point = 1 place).

Ce dépôt est un fork de [Sedrickgael/Python_Testing_2627](https://github.com/Sedrickgael/Python_Testing_2627).
Il contient la correction des bogues de la phase 1, la fonctionnalité de la phase 2
(tableau public des points) et les tests demandés (unitaires, intégration, fonctionnels
et performance), conformément aux spécifications fonctionnelles fournies.

## Sommaire

1. [Technologies](#1-technologies)
2. [Installation](#2-installation)
3. [Lancer l'application](#3-lancer-lapplication)
4. [Données](#4-données)
5. [Règles métier](#5-règles-métier)
6. [Tests](#6-tests)
7. [Tests de performance (Locust)](#7-tests-de-performance-locust)
8. [Qualité du code (flake8)](#8-qualité-du-code-flake8)
9. [Rapports](#9-rapports)
10. [Bogues corrigés et fonctionnalités](#10-bogues-corrigés-et-fonctionnalités)
11. [Conventions et organisation Git](#11-conventions-et-organisation-git)

## 1. Technologies

| Outil | Rôle | Documentation |
|---|---|---|
| Python 3.14 | Langage | https://docs.python.org/fr/3/ |
| Flask 3.1 | Framework web | https://flask.palletsprojects.com/ |
| pytest | Tests unitaires et d'intégration | https://docs.pytest.org/ |
| coverage / pytest-cov | Couverture de code | https://coverage.readthedocs.io/ |
| pytest-html | Rapport de tests HTML | https://pytest-html.readthedocs.io/ |
| Selenium + Microsoft Edge | Tests fonctionnels dans un navigateur | https://www.selenium.dev/documentation/ |
| Locust | Tests de performance | https://docs.locust.io/ |
| flake8 / flake8-html | Respect de la PEP 8 | https://flake8.pycqa.org/ |

> Les versions d'origine du `requirements.txt` (Flask 1.1.2, Werkzeug 1.0.1…) ne
> fonctionnent pas avec Python 3.12 et plus récents. Les dépendances ont donc été mises
> à jour (branche `amelioration/mise-a-jour-dependances`).

## 2. Installation

```bash
git clone https://github.com/SeydouIIT05/Python_Testing_2627.git
cd Python_Testing_2627
python -m venv .venv
```

Activer l'environnement virtuel :

- Windows (PowerShell) : `.venv\Scripts\activate`
- macOS / Linux : `source .venv/bin/activate`

Puis installer les dépendances :

```bash
pip install -r requirements.txt
```

## 3. Lancer l'application

```bash
flask --app server run
```

L'application est alors disponible sur http://127.0.0.1:5000.

Adresses e-mail utilisables pour se connecter (voir `clubs.json`) :

| Club | E-mail | Points |
|---|---|---|
| Simply Lift | john@simplylift.co | 13 |
| Iron Temple | admin@irontemple.com | 4 |
| She Lifts | kate@shelifts.co.uk | 12 |

Pages principales :

- `/` : connexion des secrétaires ;
- `/showSummary` : compétitions et points du club connecté ;
- `/book/<compétition>/<club>` : réservation de places ;
- `/pointsBoard` : tableau public des points de tous les clubs (sans connexion) ;
- `/logout` : déconnexion.

Interface : toutes les pages héritent du gabarit `templates/base.html` (en-tête,
messages, pied de page) et partagent la feuille de style `static/style.css` : coins
carrés, bleu marine (`#1F3A5F`), or sourd (`#B08D57`) et fond blanc cassé (`#F4F2EE`).
Les messages de réussite s'affichent en vert, les erreurs en brique, et chaque
compétition porte un badge d'état (*Open*, *Full* ou *Booking closed*).

## 4. Données

Pour rester léger, l'application n'utilise pas de base de données : les données sont lues
au démarrage dans deux fichiers JSON.

- `clubs.json` : les clubs, l'e-mail de leur secrétaire et leurs points ;
- `competitions.json` : les compétitions, leur date et le nombre de places.

Les réservations sont gardées en mémoire : redémarrer le serveur remet les données à
leur état initial. Les deux compétitions d'origine datant de 2020, une compétition à
venir (« Winter Classic », février 2027) a été ajoutée pour que l'application reste
utilisable.

## 5. Règles métier

Une réservation n'est acceptée que si toutes les conditions suivantes sont remplies ;
sinon, un message d'erreur explique pourquoi et rien n'est modifié.

| Règle | Message affiché en cas de refus |
|---|---|
| La compétition n'est pas passée (elle reste visible) | *Booking is closed: this competition has already taken place.* |
| Le nombre de places est un entier ≥ 1 | *Please enter a valid number of places (at least 1).* |
| Il reste assez de places dans la compétition | *Not enough places left in this competition: N available.* / *This competition is full.* |
| Le club a assez de points (1 point par place) | *Not enough points to book that many places.* |
| Un club réserve au maximum 12 places par compétition (cumulées) | *You cannot book more than 12 places per competition.* |

Après une réservation, les points utilisés sont déduits du club et les places de la
compétition, et un message confirme le nombre de places réservées. Le formulaire de
réservation limite aussi la saisie (minimum 1, maximum = places encore réservables).

## 6. Tests

Les tests sont rangés par type, comme demandé par le guide de développement :

| Dossier | Type | Nombre |
|---|---|---|
| `tests/unit/` | Tests unitaires (fonctions isolées) | 150 |
| `tests/integration/` | Tests d'intégration (routes Flask via le client de test) | 75 |
| `tests/functional/` | Tests fonctionnels (parcours complets dans Edge) | 7 |
| `tests/performance/` | Tests de performance (Locust) | – |

Les tests unitaires et d'intégration utilisent des données de test (`tests/conftest.py`)
et ne modifient jamais les fichiers JSON.

```bash
# Tous les tests
pytest

# Sans les tests fonctionnels (pas besoin de navigateur)
pytest -m "not functional"

# Un seul type de tests
pytest tests/unit

# Couverture de code
pytest --cov=server --cov-report=term-missing
```

Les tests fonctionnels pilotent Microsoft Edge sans fenêtre. Selenium télécharge
automatiquement le pilote d'Edge ; si Edge n'est pas installé, ces tests sont ignorés.

## 7. Tests de performance (Locust)

Seuils des spécifications : moins de 5 secondes pour afficher la liste des compétitions,
moins de 2 secondes pour mettre à jour les points. Le nombre d'utilisateurs par défaut
est de 6 (`tests/performance/locust.conf`). Le test se termine en erreur si un seuil
est dépassé.

Lancer l'application dans un premier terminal (`flask --app server run`), puis :

```bash
# Interface web sur http://localhost:8089
locust --config tests/performance/locust.conf

# Ou sans interface, avec rapport HTML (1 minute)
locust --config tests/performance/locust.conf --headless --html reports/performance/locust_report.html
```

Résultats obtenus (6 utilisateurs, 1 minute, 181 requêtes, 0 échec) :

| Requête | Temps moyen | Temps maximum | Seuil |
|---|---|---|---|
| Liste des compétitions | 19 ms | 143 ms | 5 000 ms |
| Réservation (mise à jour des points) | 18 ms | 40 ms | 2 000 ms |
| Tableau des points | 18 ms | 71 ms | – |

Sous cette charge, aucune surréservation ni aucun solde de points négatif n'a été observé.

## 8. Qualité du code (flake8)

La configuration se trouve dans `.flake8` (longueur de ligne maximale : 79 caractères,
environnement virtuel et rapports exclus).

```bash
flake8
flake8 --format=html --htmldir=reports/flake8
```

Résultat : 0 alerte.

## 9. Rapports

Les rapports sont générés dans le dossier `reports/` (ouvrir les fichiers HTML dans un
navigateur) :

| Rapport | Fichier | Résultat |
|---|---|---|
| Tests | `reports/tests/report.html` | 232 tests réussis |
| Couverture | `reports/coverage/index.html` | 100 % de `server.py` (objectif : 60 %) |
| Performance | `reports/performance/locust_report.html` | Seuils respectés |
| flake8 | `reports/flake8/index.html` | 0 alerte |

Pour les régénérer :

```bash
pytest --html=reports/tests/report.html --self-contained-html --cov=server --cov-report=html:reports/coverage
flake8 --format=html --htmldir=reports/flake8 --exit-zero
```

## 10. Bogues corrigés et fonctionnalités

Les issues sont celles du dépôt d'origine
[OpenClassrooms-Student-Center/Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing/issues).
Chaque correction a été faite en TDD (tests écrits d'abord) sur sa propre branche.

| Issue | Problème | Branche |
|---|---|---|
| #1 | Un e-mail inconnu fait planter l'application | `bug/unknown-email-crash` |
| #2 | Un club peut utiliser plus de points qu'il n'en a | `bug/not-enough-points` |
| #6 | Les points utilisés ne sont pas déduits | `bug/points-not-deducted` |
| #4 | Un club peut réserver plus de 12 places | `bug/max-12-places` |
| #282 | On peut réserver plus de places que celles disponibles | `bug/more-places-than-available` |
| #5 | On peut réserver une compétition passée | `bug/past-competitions` |
| – | Un nombre de places nul, négatif ou non numérique est accepté | `bug/invalid-places-input` |
| – | Un club ou une compétition inconnus font planter l'application | `bug/unknown-club-or-competition` |
| #7 | Tableau public des points des clubs | `feature/points-board` |

Améliorations :

| Branche | Contenu |
|---|---|
| `amelioration/mise-a-jour-dependances` | Dépendances compatibles Python 3.14, outils de test |
| `amelioration/booking-feedback` | Interface : confirmation du nombre de places, places encore réservables, style commun |
| `amelioration/flake8` | Correction des alertes flake8 du code d'origine |
| `amelioration/unit-tests` | Tests unitaires des cas limites |
| `amelioration/functional-tests` | Tests fonctionnels Selenium |
| `amelioration/performance-tests` | Tests de performance Locust |
| `amelioration/reports` | Rapports de tests, de couverture et flake8 |
| `amelioration/readme` | Ce README |
| `amelioration/interface-design` | Nouveau design : gabarit commun, coins carrés, palette marine et or, messages et badges colorés |

## 11. Conventions et organisation Git

- **`main`** est la source de vérité : on peut la cloner et lancer le projet à tout moment.
- **Une branche par sujet**, nommée `<type>/nom-descriptif` :
  `bug/…` pour un bogue, `feature/…` pour une fonctionnalité, `amelioration/…` pour une
  amélioration.
- Une branche n'est fusionnée dans `main` (`git merge --no-ff`) que lorsque tous les
  tests passent ; les branches sont conservées pour garder l'historique visible.
- **`QA`** est créée à partir de `main` pour la revue de code ; elle n'est jamais fusionnée
  dans `main`.
- Messages de commit en français, décrivant la correction apportée.
- Code : noms de fonctions en camelCase (style du code d'origine), constantes en
  MAJUSCULES, PEP 8 vérifiée par flake8.

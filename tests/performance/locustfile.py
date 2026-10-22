"""Tests de performance de GUDLFT avec Locust.

Seuils des spécifications (phase 2) :
- la liste des compétitions doit se charger en moins de 5 secondes ;
- la mise à jour des points (réservation) doit prendre moins de 2 secondes.

Le test échoue (code de sortie 1) si l'un de ces seuils est dépassé.
"""
import random

from locust import HttpUser, between, events, task


COMPETITIONS_LIST = "Liste des competitions"
POINTS_UPDATE = "Reservation (mise a jour des points)"
POINTS_BOARD = "Tableau des points"

MAX_COMPETITIONS_LIST_MS = 5000
MAX_POINTS_UPDATE_MS = 2000

CLUBS = [
    ("Simply Lift", "john@simplylift.co"),
    ("Iron Temple", "admin@irontemple.com"),
    ("She Lifts", "kate@shelifts.co.uk"),
]


class Secretary(HttpUser):
    """Secrétaire de club qui consulte les compétitions et réserve."""

    wait_time = between(1, 3)

    def on_start(self):
        self.club, self.email = random.choice(CLUBS)
        self.client.get("/", name="Page de connexion")

    @task(3)
    def view_competitions(self):
        self.client.post(
            "/showSummary", data={"email": self.email},
            name=COMPETITIONS_LIST,
        )

    @task(2)
    def view_points_board(self):
        self.client.get("/pointsBoard", name=POINTS_BOARD)

    @task(1)
    def book_one_place(self):
        # Une réservation refusée (points ou places épuisés) est une réponse
        # normale de l'application : seul son temps de réponse compte ici.
        with self.client.post(
            "/purchasePlaces",
            data={"club": self.club, "competition": "Winter Classic",
                  "places": 1},
            name=POINTS_UPDATE,
            catch_response=True,
        ) as response:
            if response.status_code in (200, 400):
                response.success()


@events.quitting.add_listener
def check_thresholds(environment, **kwargs):
    stats = environment.stats
    thresholds = [
        (COMPETITIONS_LIST, MAX_COMPETITIONS_LIST_MS),
        (POINTS_UPDATE, MAX_POINTS_UPDATE_MS),
    ]
    for name, limit in thresholds:
        maximum = stats.get(name, "POST").max_response_time
        if maximum > limit:
            print(f"ECHEC : {name} a pris {maximum:.0f} ms (> {limit} ms)")
            environment.process_exit_code = 1
        else:
            print(f"OK : {name} au maximum {maximum:.0f} ms (< {limit} ms)")

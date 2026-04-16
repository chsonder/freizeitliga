from player import Player
from set import Set


class Match:
    """Repräsentiert ein abgeschlossenes Best-of-Five-Match."""

    MIN_SETS = 3
    MAX_SETS = 5
    REQUIRED_WINS = 3

    def __init__(self, competitor1: list[Player], competitor2: list[Player], sets: list[Set]):
        """
        Initialisiert ein Match zwischen zwei Gegnern.

        Args:
            competitor1: Liste mit einem Spieler oder zwei Spielern für Seite 1
            competitor2: Liste mit einem Spieler oder zwei Spielern für Seite 2
            sets: Liste abgeschlossener Sätze in der Reihenfolge des Spiels

        Raises:
            TypeError: Wenn die Wettbewerber oder Sätze falsch sind
            ValueError: Wenn das Match nicht den Regeln entspricht
        """
        self._validate_competitors(competitor1, competitor2)
        self.competitor1 = competitor1
        self.competitor2 = competitor2
        self.sets = sets

        self._validate_sets()

    def _validate_competitors(self, competitor1: list[Player], competitor2: list[Player]) -> None:
        if not isinstance(competitor1, list) or not isinstance(competitor2, list):
            raise TypeError("competitor1 und competitor2 müssen Listen von Player-Instanzen sein")
        if len(competitor1) not in (1, 2) or len(competitor2) not in (1, 2):
            raise ValueError("Jede Seite muss aus einem Einzelspieler oder zwei Doppelspielern bestehen")
        if len(competitor1) != len(competitor2):
            raise ValueError("Einzelspieler dürfen nur gegen Einzelspieler und Doppel nur gegen Doppel antreten")
        if any(not isinstance(player, Player) for player in competitor1 + competitor2):
            raise TypeError("Alle Teilnehmer müssen Player-Instanzen sein")

        ids = [player.id for player in competitor1]
        for player in competitor2:
            if player.id in ids:
                raise ValueError("Ein Spieler darf nicht auf beiden Seiten desselben Matches stehen")

    def _validate_sets(self) -> None:
        if not isinstance(self.sets, list):
            raise TypeError("sets muss eine Liste von Set-Objekten sein")
        if not (self.MIN_SETS <= len(self.sets) <= self.MAX_SETS):
            raise ValueError(f"Ein Match muss zwischen {self.MIN_SETS} und {self.MAX_SETS} Sätzen haben")
        if any(not isinstance(game_set, Set) for game_set in self.sets):
            raise TypeError("Alle Elemente von sets müssen Set-Instanzen sein")

        wins1 = 0
        wins2 = 0
        for index, game_set in enumerate(self.sets, start=1):
            if not game_set.is_valid():
                raise ValueError(f"Ungültiger Satz in Position {index}: {game_set}")
            winner = game_set.winner()
            if winner == 1:
                wins1 += 1
            else:
                wins2 += 1

            if wins1 == self.REQUIRED_WINS or wins2 == self.REQUIRED_WINS:
                if index != len(self.sets):
                    raise ValueError("Es dürfen nach dem Gewinn des Matches keine weiteren Sätze eingetragen werden")

        if wins1 != self.REQUIRED_WINS and wins2 != self.REQUIRED_WINS:
            raise ValueError("Das Match muss mit genau drei gewonnenen Sätzen für einen Teilnehmer enden")

    def score(self) -> tuple[int, int]:
        """Gibt den Satzstand zurück (gewonnene Sätze Seite 1, Seite 2)."""
        wins1 = sum(1 for game_set in self.sets if game_set.winner() == 1)
        wins2 = sum(1 for game_set in self.sets if game_set.winner() == 2)
        return wins1, wins2

    def is_finished(self) -> bool:
        """Prüft, ob das Match abgeschlossen ist."""
        wins1, wins2 = self.score()
        return wins1 == self.REQUIRED_WINS or wins2 == self.REQUIRED_WINS

    def winner(self) -> list[Player]:
        """Gibt die Gewinner-Seite zurück."""
        wins1, wins2 = self.score()
        return self.competitor1 if wins1 > wins2 else self.competitor2

    def loser(self) -> list[Player]:
        """Gibt die Verlierer-Seite zurück."""
        wins1, wins2 = self.score()
        return self.competitor2 if wins1 > wins2 else self.competitor1

    def to_dict(self) -> dict:
        """Konvertiert das Match in ein Dictionary."""
        return {
            "competitor1": [player.to_dict() for player in self.competitor1],
            "competitor2": [player.to_dict() for player in self.competitor2],
            "sets": [game_set.to_dict() for game_set in self.sets],
            "score": self.score(),
        }

    def __repr__(self) -> str:
        score1, score2 = self.score()
        return f"Match({score1}:{score2}, sets={len(self.sets)})"

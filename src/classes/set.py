class Set:
    """Repräsentiert einen abgeschlossenen Satz in einem Tischtennis-Match."""

    def __init__(self, points1: int, points2: int):
        """
        Initialisiert einen Satz mit Punktwerten für beide Seiten.

        Args:
            points1: Punkte von Spieler 1 bzw. Seite 1
            points2: Punkte von Spieler 2 bzw. Seite 2

        Raises:
            TypeError: Wenn Punkte keine Ganzzahlen sind
            ValueError: Wenn Punkte keinen gültigen Satz ergeben
        """
        if not isinstance(points1, int) or not isinstance(points2, int):
            raise TypeError("Punktzahlen müssen ganze Zahlen sein")
        if points1 < 0 or points2 < 0:
            raise ValueError("Punkte müssen größer gleich 0 sein")

        self.points1 = points1
        self.points2 = points2

        if not self.is_valid():
            raise ValueError(f"Ungültiges Satz-Ergebnis: {points1}:{points2}")

    def is_valid(self) -> bool:
        """Prüft, ob das Satz-Ergebnis den Regeln entspricht."""
        if self.points1 == self.points2:
            return False

        high_score = max(self.points1, self.points2)
        low_score = min(self.points1, self.points2)

        if high_score < 11:
            return False
        if high_score == 11:
            return low_score <= 9

        return high_score >= 12 and high_score - low_score == 2

    def winner(self) -> int:
        """Gibt den Satzgewinner zurück: 1 oder 2."""
        if not self.is_valid():
            raise ValueError("Satz ist nicht gültig")
        return 1 if self.points1 > self.points2 else 2

    def to_dict(self) -> dict:
        """Konvertiert den Satz in ein Dictionary."""
        return {
            "points1": self.points1,
            "points2": self.points2,
        }

    def __repr__(self) -> str:
        return f"Set({self.points1}:{self.points2})"

from uuid import UUID, uuid4

from team import Team


class League:
    """Repräsentiert eine Liga in der Freizeitliga."""

    def __init__(self, name: str):
        """
        Initialisiert eine neue Liga mit automatisch generierter UUID.

        Args:
            name: Name der Liga

        Raises:
            TypeError: Wenn name kein nicht-leerer String ist
        """
        if not isinstance(name, str) or not name.strip():
            raise TypeError("name muss ein nicht-leerer String sein")

        self.id: UUID = uuid4()
        self.name: str = name.strip()
        self._teams: list[Team] = []

    def __repr__(self) -> str:
        """Gibt eine String-Repräsentation der Liga zurück."""
        return f"League(id={self.id}, name='{self.name}', teams={len(self._teams)})"

    def __str__(self) -> str:
        """Gibt den Namen der Liga zurück."""
        return self.name

    def add_team(self, team: Team) -> None:
        """
        Fügt ein Team zur Liga hinzu.

        Args:
            team: Ein Team-Objekt

        Raises:
            TypeError: Wenn team keine Team-Instanz ist
            ValueError: Wenn ein Team mit dieser UUID bereits in der Liga ist
        """
        if not isinstance(team, Team):
            raise TypeError("team muss eine Instanz der Team-Klasse sein")
        if any(t.id == team.id for t in self._teams):
            raise ValueError(f"Team mit ID {team.id} ist bereits in der Liga")

        self._teams.append(team)

    def remove_team(self, team: Team) -> None:
        """
        Entfernt ein Team aus der Liga anhand seiner UUID.

        Args:
            team: Das zu entfernende Team

        Raises:
            ValueError: Wenn kein Team mit dieser UUID in der Liga ist
        """
        for i, t in enumerate(self._teams):
            if t.id == team.id:
                self._teams.pop(i)
                return
        raise ValueError(f"Team mit ID {team.id} ist nicht in der Liga")

    def get_teams(self) -> list[Team]:
        """Gibt die Teams der Liga zurück."""
        return self._teams.copy()

    def get_team_count(self) -> int:
        """Gibt die Anzahl der Teams in der Liga zurück."""
        return len(self._teams)

    def to_dict(self) -> dict:
        """Konvertiert die Liga in ein Dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "teams": [team.to_dict() for team in self._teams],
        }

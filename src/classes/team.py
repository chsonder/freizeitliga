from uuid import UUID, uuid4

from player import Player


class Team:
    """Repräsentiert ein Team in der Freizeitliga."""

    def __init__(self, name: str):
        """
        Initialisiert ein neues Team mit automatisch generierter UUID.

        Args:
            name: Name des Teams

        Raises:
            TypeError: Wenn name kein nicht-leerer String ist
        """
        if not isinstance(name, str) or not name.strip():
            raise TypeError("name muss ein nicht-leerer String sein")

        self.id: UUID = uuid4()
        self.name: str = name.strip()
        self._players: list[Player] = []

    def __repr__(self) -> str:
        """Gibt eine String-Repräsentation des Teams zurück."""
        return f"Team(id={self.id}, name='{self.name}', spieler={len(self._players)})"

    def __str__(self) -> str:
        """Gibt den Namen des Teams zurück."""
        return self.name

    def add_player(self, player: Player) -> None:
        """
        Fügt einen Spieler zur Aufstellung hinzu.

        Args:
            player: Ein Player-Objekt

        Raises:
            TypeError: Wenn player keine Player-Instanz ist
            ValueError: Wenn ein Spieler mit dieser UUID bereits im Team ist
        """
        if not isinstance(player, Player):
            raise TypeError("player muss eine Instanz der Player-Klasse sein")
        if any(p.id == player.id for p in self._players):
            raise ValueError(f"Spieler mit ID {player.id} ist bereits im Team")

        self._players.append(player)

    def remove_player(self, player: Player) -> None:
        """
        Entfernt einen Spieler aus der Aufstellung anhand seiner UUID.

        Args:
            player: Der zu entfernende Spieler

        Raises:
            ValueError: Wenn kein Spieler mit dieser UUID im Team ist
        """
        for i, p in enumerate(self._players):
            if p.id == player.id:
                self._players.pop(i)
                return
        raise ValueError(f"Spieler mit ID {player.id} ist nicht im Team")

    def get_aufstellung(self) -> list[Player]:
        """Gibt die Aufstellung (Spieler in Reihenfolge) zurück."""
        return self._players.copy()

    def is_vollstaendig(self) -> bool:
        """Prüft, ob das Team mindestens 4 Spieler hat."""
        return len(self._players) >= 4

    def to_dict(self) -> dict:
        """Konvertiert das Team in ein Dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "aufstellung": [player.to_dict() for player in self._players],
        }

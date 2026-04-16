from uuid import UUID, uuid4


class Player:
    """Repräsentiert einen Spieler in der Freizeitliga."""

    def __init__(self, name: str, vorname: str, qttr: int):
        """
        Initialisiert einen neuen Spieler mit automatisch generierter UUID.

        Args:
            name: Nachname des Spielers
            vorname: Vorname des Spielers
            qttr: QTTR (Quartals-Tischtennis-Rating) - positive Ganzzahl

        Raises:
            ValueError: Wenn QTTR keine positive Ganzzahl ist
            TypeError: Wenn name oder vorname keine Strings sind
        """
        if not isinstance(name, str) or not name.strip():
            raise TypeError("name muss ein nicht-leerer String sein")
        if not isinstance(vorname, str) or not vorname.strip():
            raise TypeError("vorname muss ein nicht-leerer String sein")
        if not isinstance(qttr, int) or qttr <= 0:
            raise ValueError("qttr muss eine positive Ganzzahl sein")

        self.id: UUID = uuid4()
        self.name: str = name.strip()
        self.vorname: str = vorname.strip()
        self.qttr: int = qttr

    def __repr__(self) -> str:
        """Gibt eine String-Repräsentation des Spielers zurück."""
        return f"Player(id={self.id}, name='{self.name}', vorname='{self.vorname}', qttr={self.qttr})"

    def __str__(self) -> str:
        """Gibt den vollständigen Namen des Spielers zurück."""
        return f"{self.vorname} {self.name}"

    def to_dict(self) -> dict:
        """Konvertiert den Spieler in ein Dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "vorname": self.vorname,
            "qttr": self.qttr,
        }

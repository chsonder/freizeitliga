from .team import Team
from .match import Match
from .player import Player


class TeamTie:
    """Repräsentiert einen Mannschaftskampf zwischen zwei Teams."""

    REQUIRED_MATCH_COUNT = 6
    DOUBLE_MATCHES = 2
    SINGLE_MATCHES = 4

    def __init__(self, team1: Team, team2: Team, matches: list[Match]):
        """
        Initialisiert einen Mannschaftskampf mit zwei Teams und genau sechs Matches.

        Args:
            team1: Heimteam
            team2: Gastteam
            matches: Liste mit genau 6 Matches in der Reihenfolge: zwei Doppel, vier Einzel

        Raises:
            TypeError: Bei falschen Typen
            ValueError: Bei Regelverstößen
        """
        if not isinstance(team1, Team) or not isinstance(team2, Team):
            raise TypeError("team1 und team2 müssen Team-Instanzen sein")
        if team1.id == team2.id:
            raise ValueError("team1 und team2 dürfen nicht dasselbe Team sein")
        if not isinstance(matches, list):
            raise TypeError("matches muss eine Liste von Match-Instanzen sein")
        if len(matches) != self.REQUIRED_MATCH_COUNT:
            raise ValueError(f"Ein Mannschaftskampf muss genau {self.REQUIRED_MATCH_COUNT} Matches enthalten")
        if any(not isinstance(match, Match) for match in matches):
            raise TypeError("Alle Elemente in matches müssen Match-Instanzen sein")

        self.team1 = team1
        self.team2 = team2
        self.matches = matches

        self._validate_match_order()
        self._validate_team_players()

    def _validate_match_order(self) -> None:
        for index, match in enumerate(self.matches):
            expected_size = 2 if index < self.DOUBLE_MATCHES else 1
            if len(match.competitor1) != expected_size or len(match.competitor2) != expected_size:
                kind = "Doppel" if expected_size == 2 else "Einzel"
                raise ValueError(f"Match {index + 1} muss ein {kind} sein")

    def _validate_team_players(self) -> None:
        self._validate_matches_belong_to_teams()
        self._validate_double_players()
        self._validate_single_players_order()

    def _validate_matches_belong_to_teams(self) -> None:
        team1_ids = [player.id for player in self.team1.get_aufstellung()]
        team2_ids = [player.id for player in self.team2.get_aufstellung()]

        for index, match in enumerate(self.matches, start=1):
            for player in match.competitor1:
                if player.id not in team1_ids:
                    raise ValueError(f"Spieler in Match {index} auf Team1-Seite gehört nicht zu team1")
            for player in match.competitor2:
                if player.id not in team2_ids:
                    raise ValueError(f"Spieler in Match {index} auf Team2-Seite gehört nicht zu team2")

    def _validate_double_players(self) -> None:
        double_players1 = []
        double_players2 = []

        for match in self.matches[: self.DOUBLE_MATCHES]:
            double_players1.extend(match.competitor1)
            double_players2.extend(match.competitor2)

        if len({player.id for player in double_players1}) != 4:
            raise ValueError("Die beiden Doppel von team1 müssen von vier unterschiedlichen Spielern bestritten werden")
        if len({player.id for player in double_players2}) != 4:
            raise ValueError("Die beiden Doppel von team2 müssen von vier unterschiedlichen Spielern bestritten werden")

    def _validate_single_players_order(self) -> None:
        single_players1 = [match.competitor1[0] for match in self.matches[self.DOUBLE_MATCHES :]]
        single_players2 = [match.competitor2[0] for match in self.matches[self.DOUBLE_MATCHES :]]

        self._validate_distinct_single_players(single_players1, "team1")
        self._validate_distinct_single_players(single_players2, "team2")

        self._validate_order_against_team(single_players1, self.team1, "team1")
        self._validate_order_against_team(single_players2, self.team2, "team2")

    def _validate_distinct_single_players(self, players: list[Player], team_name: str) -> None:
        if len({player.id for player in players}) != self.SINGLE_MATCHES:
            raise ValueError(f"Die vier Einzel von {team_name} müssen von vier unterschiedlichen Spielern bestritten werden")

    def _validate_order_against_team(self, players: list[Player], team: Team, team_name: str) -> None:
        order_map = {player.id: index for index, player in enumerate(team.get_aufstellung())}
        indices = [order_map[player.id] for player in players]
        if indices != sorted(indices):
            raise ValueError(f"Die Einzelreihenfolge von {team_name} muss der Team-Aufstellung entsprechen")

    def team_score(self) -> tuple[int, int]:
        """Gibt den Satzstand des Mannschaftskampfs zurück."""
        wins1 = sum(1 for match in self.matches if match.winner() == match.competitor1)
        wins2 = self.REQUIRED_MATCH_COUNT - wins1
        return wins1, wins2

    def team_points(self) -> tuple[int, int]:
        """Gibt die Mannschaftspunkte für team1 und team2 zurück."""
        wins1, wins2 = self.team_score()
        if wins1 > wins2:
            return 2, 0
        if wins1 < wins2:
            return 0, 2
        return 1, 1

    def winner(self) -> Team | None:
        """Gibt das siegreiche Team zurück oder None bei Unentschieden."""
        wins1, wins2 = self.team_score()
        if wins1 > wins2:
            return self.team1
        if wins2 > wins1:
            return self.team2
        return None

    def to_dict(self) -> dict:
        return {
            "team1": self.team1.to_dict(),
            "team2": self.team2.to_dict(),
            "matches": [match.to_dict() for match in self.matches],
        }
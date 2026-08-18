from distance import Distance


class Trail:
    """Represents a hiking trail with a name, distance, elevation gain,
    and a difficulty level guarded by validation."""

    DEFAULT_UNIT = "km"
    VALID_DIFFICULTIES = ("easy", "moderate", "hard")

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty):
        self._trail_id = trail_id
        self._name = name
        self._distance = distance
        self._elevation_gain_m = elevation_gain_m
        self._difficulty = None
        self.set_difficulty(difficulty)

    # ---- properties (read access to protected state) ----
    @property
    def trail_id(self):
        return self._trail_id

    @property
    def name(self):
        return self._name

    @property
    def distance(self):
        return self._distance

    @property
    def elevation_gain_m(self):
        return self._elevation_gain_m

    @property
    def difficulty(self):
        return self._difficulty

    # ---- guarded state change ----
    def set_difficulty(self, difficulty):
        if not self._valid_difficulty(difficulty):
            raise ValueError(f"Difficulty must be one of {self.VALID_DIFFICULTIES}.")
        self._difficulty = difficulty

    # ---- WP-103: static validator ----
    @staticmethod
    def _valid_difficulty(difficulty):
        return difficulty in Trail.VALID_DIFFICULTIES

    @staticmethod
    def _valid_distance(magnitude):
        return magnitude >= 0

    # ---- WP-103: alternate constructor from an API-shaped dict ----
    @classmethod
    def from_dict(cls, data):
        """Build a Trail from a dict like:
        {"id": 1, "name": "Bruce Trail", "distance_km": 12.5,
         "elevation_gain_m": 300, "difficulty": "moderate"}
        """
        if not cls._valid_distance(data["distance_km"]):
            raise ValueError("Distance magnitude cannot be negative.")
        distance = Distance(data["distance_km"], cls.DEFAULT_UNIT)
        return cls(
            trail_id=data["id"],
            name=data["name"],
            distance=distance,
            elevation_gain_m=data["elevation_gain_m"],
            difficulty=data["difficulty"],
        )

    # ---- WP-104: equality based on id ----
    def __eq__(self, other):
        if not isinstance(other, Trail):
            return NotImplemented
        return self._trail_id == other._trail_id

    def __repr__(self):
        return f"Trail({self._trail_id!r}, {self._name!r}, {self._distance.magnitude}{self._distance.unit})"
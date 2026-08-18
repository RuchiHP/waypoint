from abc import ABC, abstractmethod
from distance import Distance


class Trail(ABC):
    """Abstract base for all trail types. Subclasses must implement
    estimated_time() and summary(), since how a trail's time and
    summary are computed genuinely differs by trail type."""

    DEFAULT_UNIT = "km"
    VALID_DIFFICULTIES = ("easy", "moderate", "hard")

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty):
        self._trail_id = trail_id
        self._name = name
        self._distance = distance
        self._elevation_gain_m = elevation_gain_m
        self._difficulty = None
        self.set_difficulty(difficulty)

    # ---- properties ----
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

    def packing_list(self):
        """Default packing list. Subclasses that need more should
        call super().packing_list() and extend it, not replace it."""
        return ["map", "water", "first aid kit"]

    @staticmethod
    def _valid_difficulty(difficulty):
        return difficulty in Trail.VALID_DIFFICULTIES

    @staticmethod
    def _valid_distance(magnitude):
        return magnitude >= 0

    # ---- WP-201: abstract methods every trail type must implement ----
    @abstractmethod
    def estimated_time(self):
        """Return estimated completion time in hours (float)."""
        raise NotImplementedError

    @abstractmethod
    def summary(self):
        """Return a short human-readable description of the trail."""
        raise NotImplementedError

    # ---- alternate constructor from an API-shaped dict ----
    @classmethod
    def from_dict(cls, data):
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

    # ---- equality based on id ----
    def __eq__(self, other):
        if not isinstance(other, Trail):
            return NotImplemented
        return self._trail_id == other._trail_id

    def __hash__(self):
        return hash(self._trail_id)

    def __repr__(self):
        return f"{type(self).__name__}({self._trail_id!r}, {self._name!r}, {self._distance.magnitude}{self._distance.unit})"
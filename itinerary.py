from distance import Distance


class Itinerary:
    """A named, ordered collection of trails (composition: HAS-A trails)."""

    def __init__(self, name):
        self._name = name
        self._trails = []  # each Itinerary owns its own list

    @property
    def name(self):
        return self._name

    @property
    def trails(self):
        # return a copy so callers can't mutate our internal list directly
        return list(self._trails)

    def add_trail(self, trail):
        self._trails.append(trail)

    def total_distance(self):
        """Sum all trail distances, returned as a Distance in the
        platform default unit."""
        if not self._trails:
            return Distance(0, "km")

        total_km = 0
        for trail in self._trails:
            d = trail.distance
            if d.unit == "km":
                total_km += d.magnitude
            else:
                total_km += d.convert("km").magnitude

        return Distance(total_km, "km")

    def __repr__(self):
        return f"Itinerary({self._name!r}, {len(self._trails)} trails)"


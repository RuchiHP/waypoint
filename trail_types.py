from trail import Trail


# ---- WP-201: concrete trail types with their own pacing ----

class DayHike(Trail):
    """A single-day hike. Pace slows on steep elevation gain."""

    BASE_PACE_KMH = 4.0  # flat-ground walking pace

    def estimated_time(self):
        km = self._distance.convert("km").magnitude
        flat_hours = km / self.BASE_PACE_KMH
        # Naismith's-rule-style: add ~1 hour per 600m of elevation gain
        elevation_hours = self._elevation_gain_m / 600
        return round(flat_hours + elevation_hours, 2)

    def summary(self):
        return f"{self._name}: a {self._distance} day hike, ~{self.estimated_time()}h."

    # No packing_list override here -- DayHike uses Trail's base list as-is.


class BackpackingRoute(Trail):
    """A multi-day route. Slower pace due to pack weight, spans several days."""

    BASE_PACE_KMH = 2.5

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, days):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self._days = days

    @property
    def days(self):
        return self._days

    def estimated_time(self):
        km = self._distance.convert("km").magnitude
        flat_hours = km / self.BASE_PACE_KMH
        elevation_hours = self._elevation_gain_m / 400  # heavier pack, steeper cost
        return round(flat_hours + elevation_hours, 2)

    def summary(self):
        return f"{self._name}: a {self._days}-day backpacking route, ~{self.estimated_time()}h total."

    # ---- WP-204: override that EXTENDS the base via super(), doesn't replace it ----
    def packing_list(self):
        return super().packing_list() + ["tent", "sleeping bag", "stove", "extra food"]


class TrailRun(Trail):
    """A trail running route. Much faster pace than walking."""

    BASE_PACE_KMH = 9.0

    def estimated_time(self):
        km = self._distance.convert("km").magnitude
        flat_hours = km / self.BASE_PACE_KMH
        elevation_hours = self._elevation_gain_m / 900  # runners handle grade better than hikers
        return round(flat_hours + elevation_hours, 2)

    def summary(self):
        return f"{self._name}: a {self._distance} trail run, ~{self.estimated_time()}h."

    # ---- WP-204: this one genuinely replaces the base list, no super() call ----
    def packing_list(self):
        return ["water", "energy gel", "phone"]


# ---- WP-203: one further inheritance level ----

class GuidedDayHike(DayHike):
    """A DayHike led by a guide. Adds a guide_name field."""

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, guide_name):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self._guide_name = guide_name

    @property
    def guide_name(self):
        return self._guide_name

    def summary(self):
        # extends DayHike.summary() rather than replacing it
        return super().summary() + f" Guided by {self._guide_name}."


# ---- WP-205: mixins ----

class ElevationMixin:
    """Adds a grade_percent calculation. Expects self._distance and
    self._elevation_gain_m to exist (provided by Trail)."""

    def grade_percent(self):
        km = self._distance.convert("km").magnitude
        if km == 0:
            return 0.0
        distance_m = km * 1000
        return round((self._elevation_gain_m / distance_m) * 100, 2)


class RatingMixin:
    """Adds star-rating tracking. Independent of Trail's own state."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ratings = []

    def add_rating(self, stars):
        if not (1 <= stars <= 5):
            raise ValueError("Rating must be between 1 and 5 stars.")
        self._ratings.append(stars)

    def average_rating(self):
        if not self._ratings:
            return None
        return round(sum(self._ratings) / len(self._ratings), 2)


class RatedGuidedDayHike(ElevationMixin, RatingMixin, GuidedDayHike):
    """Composes both mixins into a guided day hike.

    MRO (via RatedGuidedDayHike.__mro__):
    RatedGuidedDayHike -> ElevationMixin -> RatingMixin -> GuidedDayHike
    -> DayHike -> Trail -> ABC -> object

    Why: Python resolves left-to-right per the class's own bases list,
    then depth-first but respecting each class's own MRO (C3 linearization).
    ElevationMixin and RatingMixin are listed first, so their methods
    (grade_percent, add_rating) take priority over anything with the same
    name further down the chain -- but neither mixin defines summary() or
    estimated_time(), so those calls fall through to GuidedDayHike/DayHike.
    RatingMixin.__init__ calls super().__init__(*args, **kwargs), which
    -- thanks to the MRO -- forwards to GuidedDayHike.__init__, not object,
    so the full init chain runs correctly even though RatingMixin doesn't
    know about GuidedDayHike directly.
    """
    pass


# ---- WP-206: duck-typed class, not inheriting Trail at all ----

class FakeTrail:
    """A duck-typed stand-in for testing the polymorphic loop.
    Implements estimated_time() and summary() without inheriting Trail."""

    def __init__(self, name, hours):
        self.name = name
        self._hours = hours

    def estimated_time(self):
        return self._hours

    def summary(self):
        return f"{self.name}: a fake trail for testing, {self._hours}h."
class Distance:
    """A value type representing a distance with a magnitude and a unit.

    Design decision (WP-202): arithmetic and comparison operators REJECT
    mixed units rather than silently auto-converting. Silently converting
    could hide unit-mismatch bugs (e.g. accidentally adding km to mi).
    If you want to combine distances in different units, convert()
    explicitly first, then operate.
    """

    VALID_UNITS = ("km", "mi")

    def __init__(self, magnitude, unit):
        if magnitude < 0:
            raise ValueError("Distance magnitude cannot be negative.")
        if unit not in self.VALID_UNITS:
            raise ValueError(f"Unit must be one of {self.VALID_UNITS}.")
        self._magnitude = magnitude
        self._unit = unit

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def unit(self):
        return self._unit

    def convert(self, to_unit):
        """Return a new Distance converted to the other unit."""
        if to_unit not in self.VALID_UNITS:
            raise ValueError(f"Unit must be one of {self.VALID_UNITS}.")
        if to_unit == self._unit:
            return Distance(self._magnitude, self._unit)

        if self._unit == "km" and to_unit == "mi":
            new_magnitude = self._magnitude * 0.621371
        elif self._unit == "mi" and to_unit == "km":
            new_magnitude = self._magnitude / 0.621371
        else:
            raise ValueError("Unsupported unit conversion.")

        return Distance(new_magnitude, to_unit)

    # ---- WP-202: operator overloading ----
    def _check_same_unit(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        if self._unit != other._unit:
            raise ValueError(
                f"Cannot operate on mixed units ({self._unit} vs {other._unit}). "
                f"Call .convert() first."
            )
        return None

    def __add__(self, other):
        result = self._check_same_unit(other)
        if result is NotImplemented:
            return NotImplemented
        return Distance(self._magnitude + other._magnitude, self._unit)

    def __sub__(self, other):
        result = self._check_same_unit(other)
        if result is NotImplemented:
            return NotImplemented
        new_magnitude = self._magnitude - other._magnitude
        if new_magnitude < 0:
            raise ValueError("Resulting distance cannot be negative.")
        return Distance(new_magnitude, self._unit)

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented
        return self._unit == other._unit and self._magnitude == other._magnitude

    def __lt__(self, other):
        result = self._check_same_unit(other)
        if result is NotImplemented:
            return NotImplemented
        return self._magnitude < other._magnitude

    def __gt__(self, other):
        result = self._check_same_unit(other)
        if result is NotImplemented:
            return NotImplemented
        return self._magnitude > other._magnitude

    def __hash__(self):
        return hash((self._magnitude, self._unit))

    def __str__(self):
        return f"{self._magnitude:.2f} {self._unit}"

    def __repr__(self):
        return f"Distance({self._magnitude!r}, {self._unit!r})"

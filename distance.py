class Distance:
    """A value type representing a distance with a magnitude and a unit."""

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
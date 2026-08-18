from distance import Distance
from trail import Trail
from itinerary import Itinerary

# 1. Distance rejects negative magnitude
try:
    Distance(-5, "km")
    print("FAIL: negative distance did not raise")
except ValueError:
    print("PASS: negative distance raises ValueError")

# 2. convert() round-trips within tolerance
d = Distance(10, "km")
back = d.convert("mi").convert("km")
print("PASS: convert round-trip" if abs(back.magnitude - 10) < 0.01 else "FAIL: round-trip")

# 3. Trail.from_dict populates correctly
data = {"id": 1, "name": "Bruce Trail", "distance_km": 12.5,
        "elevation_gain_m": 300, "difficulty": "moderate"}
t1 = Trail.from_dict(data)
print("PASS: from_dict" if t1.name == "Bruce Trail" and t1.distance.magnitude == 12.5 else "FAIL: from_dict")

# 4. Invalid difficulty raises ValueError
try:
    Trail(2, "Test", Distance(5, "km"), 100, "extreme")
    print("FAIL: invalid difficulty did not raise")
except ValueError:
    print("PASS: invalid difficulty raises ValueError")

# 5. Two trails, same id, different data -> equal
t2 = Trail(1, "Different Name", Distance(99, "km"), 999, "hard")
print("PASS: __eq__ by id" if t1 == t2 else "FAIL: __eq__ by id")

# 6. Itinerary total_distance and isolation between instances
trip1 = Itinerary("Weekend Trip")
trip1.add_trail(Trail(3, "A", Distance(5, "km"), 100, "easy"))
trip1.add_trail(Trail(4, "B", Distance(3, "km"), 50, "easy"))
trip1.add_trail(Trail(5, "C", Distance(2, "km"), 20, "easy"))
print("PASS: total_distance" if abs(trip1.total_distance().magnitude - 10) < 0.01 else "FAIL: total_distance")

trip2 = Itinerary("Solo Hike")
trip2.add_trail(Trail(6, "D", Distance(1, "km"), 10, "easy"))
print("PASS: itinerary isolation" if len(trip1.trails) == 3 and len(trip2.trails) == 1 else "FAIL: isolation")

# 7. Changing default unit affects new trails only
old_default = Trail.DEFAULT_UNIT
Trail.DEFAULT_UNIT = "mi"
data2 = {"id": 7, "name": "New Default Test", "distance_km": 4,
         "elevation_gain_m": 50, "difficulty": "easy"}
t3 = Trail.from_dict(data2)
print("PASS: default unit change" if t3.distance.unit == "mi" and t1.distance.unit == "km" else "FAIL: default unit change")
Trail.DEFAULT_UNIT = old_default

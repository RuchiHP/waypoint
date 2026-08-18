from waypoint_core.distance import Distance
from waypoint_core.trail import Trail
from waypoint_core.trail_types import (
    DayHike, BackpackingRoute, TrailRun, GuidedDayHike,
    RatedGuidedDayHike, FakeTrail,
)

# 1. Instantiating Trail directly raises TypeError (it's abstract)
try:
    Trail(1, "X", Distance(1, "km"), 0, "easy")
    print("FAIL: Trail instantiated directly")
except TypeError:
    print("PASS: Trail() raises TypeError (abstract)")

# 2. A subclass missing estimated_time/summary also raises TypeError
try:
    class IncompleteTrail(Trail):
        pass
    IncompleteTrail(1, "X", Distance(1, "km"), 0, "easy")
    print("FAIL: incomplete subclass instantiated")
except TypeError:
    print("PASS: incomplete subclass raises TypeError")

# 3. Distance arithmetic
d1 = Distance(3, "km")
d2 = Distance(2, "km")
print("PASS: Distance addition" if (d1 + d2) == Distance(5, "km") else "FAIL: addition")

# 4. Sorting with
distances = [Distance(5, "km"), Distance(1, "km"), Distance(3, "km")]
sorted_ds = sorted(distances)
print("PASS: sort with <" if [d.magnitude for d in sorted_ds] == [1, 3, 5] else "FAIL: sort")

# 5. Mixed units rejected (documented behavior)
try:
    Distance(1, "km") + Distance(1, "mi")
    print("FAIL: mixed units did not raise")
except ValueError:
    print("PASS: mixed units raise ValueError (documented)")

# 6. Polymorphic loop over mixed trail types, including duck-typed FakeTrail
trails = [
    DayHike(1, "Ridge Trail", Distance(10, "km"), 300, "moderate"),
    BackpackingRoute(2, "Coastal Route", Distance(40, "km"), 1200, "hard", days=3),
    TrailRun(3, "Sprint Loop", Distance(8, "km"), 100, "easy"),
    GuidedDayHike(4, "Waterfall Walk", Distance(6, "km"), 150, "easy", guide_name="Sam"),
    FakeTrail("Test Trail", 2.5),
]
print("\n-- Mixed trail list (WP-206) --")
all_ran = True
for t in trails:
    try:
        print(f"{t.__class__.__name__}: {t.estimated_time()}h")
    except Exception as e:
        all_ran = False
        print(f"FAIL: {t} raised {e}")
print("PASS: polymorphic loop ran for all types" if all_ran else "FAIL: loop")

# 7. MRO of a composed trail type
rated = RatedGuidedDayHike(5, "Alpine Loop", Distance(12, "km"), 900, "hard", guide_name="Priya")
rated.add_rating(5)
rated.add_rating(4)
print("\n-- MRO of RatedGuidedDayHike --")
print([cls.__name__ for cls in RatedGuidedDayHike.__mro__])
print("PASS: grade_percent works" if rated.grade_percent() > 0 else "FAIL: grade_percent")
print("PASS: average_rating works" if rated.average_rating() == 4.5 else "FAIL: average_rating")

# 8. FakeTrail runs unchanged through the polymorphic loop (already proven above)
fake = FakeTrail("Duck Trail", 1.0)
print("PASS: FakeTrail duck-types correctly" if fake.estimated_time() == 1.0 and fake.summary() else "FAIL: FakeTrail")

# 9. packing_list override extends rather than replaces
dh = DayHike(6, "Simple Trail", Distance(5, "km"), 50, "easy")
bp = BackpackingRoute(7, "Long Trail", Distance(30, "km"), 500, "hard", days=2)
print("PASS: packing_list extends base" if set(dh.packing_list()).issubset(set(bp.packing_list())) else "FAIL: packing_list")

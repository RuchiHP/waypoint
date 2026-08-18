from django.db import models


class Park(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("expert", "Expert"),
    ]

    name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="easy")
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    # WP-702: on_delete=SET_NULL keeps the trail record if its park is
    # deleted, rather than deleting the trail too (CASCADE) or blocking
    # the park deletion (PROTECT). A trail losing its park association
    # is acceptable data loss; losing the whole trail record is not.
    # null=True/blank=True lets existing rows (created before this field
    # existed) default to "no park" instead of breaking the migration.
    park = models.ForeignKey(Park, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
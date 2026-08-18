from django.test import TestCase, RequestFactory
from django.http import Http404
from .models import Trail
from . import views


class TrailCatalogTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Trail.objects.create(
            name="Open Easy Trail", distance_km=5.0, elevation_gain=50,
            difficulty="easy", is_open=True,
        )
        Trail.objects.create(
            name="Closed Trail", distance_km=3.0, elevation_gain=30,
            difficulty="easy", is_open=False,
        )

    def test_catalog_shows_only_open_trails(self):
        """WP-801: the open-trails query only returns open trails."""
        request = self.factory.get("/trails/")
        response = views.catalog(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Open Easy Trail", response.content)
        self.assertNotIn(b"Closed Trail", response.content)

    def test_unknown_park_raises_404(self):
        """WP-801: requesting a park id that doesn't exist raises Http404."""
        request = self.factory.get("/trails/park/9999/")
        with self.assertRaises(Http404):
            views.by_park(request, park_id=9999)

from django.test import TestCase
from tours.constants import HOME_LOCATIONS, AVERAGE_SPEED_KMH
from tours.views import haversine_distance
import math


class ConstantsTest(TestCase):
    """Test cases for constants and utility functions"""

    def test_home_locations_structure(self):
        """Test that HOME_LOCATIONS has correct structure"""
        required_keys = ['cardiff', 'barry', 'waverley', 'college-fields']

        for key in required_keys:
            self.assertIn(key, HOME_LOCATIONS)
            home = HOME_LOCATIONS[key]

            # Check required fields
            self.assertIn('name', home)
            self.assertIn('address', home)
            self.assertIn('coordinates', home)
            self.assertIn('phone', home)

            # Check coordinates format
            coords = home['coordinates']
            self.assertIsInstance(coords, tuple)
            self.assertEqual(len(coords), 2)
            self.assertIsInstance(coords[0], (int, float))  # latitude
            self.assertIsInstance(coords[1], (int, float))  # longitude

    def test_home_locations_coordinates_reasonable(self):
        """Test that coordinates are in reasonable range for UK"""
        for home_key, home_data in HOME_LOCATIONS.items():
            lat, lon = home_data['coordinates']

            # UK latitude range (roughly)
            self.assertGreaterEqual(lat, 49.0)
            self.assertLessEqual(lat, 61.0)

            # UK longitude range (roughly)
            self.assertGreaterEqual(lon, -8.0)
            self.assertLessEqual(lon, 2.0)

    def test_average_speed_constant(self):
        """Test that AVERAGE_SPEED_KMH is reasonable"""
        self.assertIsInstance(AVERAGE_SPEED_KMH, (int, float))
        self.assertGreater(AVERAGE_SPEED_KMH, 0)
        self.assertLessEqual(AVERAGE_SPEED_KMH, 100)  # Reasonable speed limit


class HaversineDistanceTest(TestCase):
    """Test cases for haversine_distance function"""

    def test_same_location_distance_zero(self):
        """Test that distance between same point is zero"""
        lat, lon = 51.4816, -3.1791  # Cardiff coordinates
        distance = haversine_distance(lat, lon, lat, lon)
        self.assertAlmostEqual(distance, 0, places=5)

    def test_known_distances(self):
        """Test distance calculations for known locations"""
        # Cardiff to Barry (approximate real distance)
        cardiff_lat, cardiff_lon = 51.4816, -3.1791
        barry_lat, barry_lon = 51.3998, -3.2826

        distance = haversine_distance(cardiff_lat, cardiff_lon, barry_lat, barry_lon)

        # Should be around 10-15 miles
        self.assertGreater(distance, 5)
        self.assertLess(distance, 25)

    def test_symmetry(self):
        """Test that distance is symmetric"""
        lat1, lon1 = 51.4816, -3.1791
        lat2, lon2 = 51.3998, -3.2826

        distance1 = haversine_distance(lat1, lon1, lat2, lon2)
        distance2 = haversine_distance(lat2, lon2, lat1, lon1)

        self.assertAlmostEqual(distance1, distance2, places=5)

    def test_equator_distance(self):
        """Test distance calculation near equator"""
        # Points 1 degree apart at equator should be ~69 miles
        lat1, lon1 = 0, 0
        lat2, lon2 = 0, 1

        distance = haversine_distance(lat1, lon1, lat2, lon2)
        expected_distance = 69.0976  # Approximate miles for 1 degree at equator

        self.assertAlmostEqual(distance, expected_distance, places=1)

    def test_pole_distance(self):
        """Test distance calculation near poles"""
        # Points 1 degree apart at high latitude
        lat1, lon1 = 89, 0
        lat2, lon2 = 89, 1

        distance = haversine_distance(lat1, lon1, lat2, lon2)

        # Should be much smaller than at equator
        self.assertLess(distance, 5)

    def test_edge_cases(self):
        """Test edge cases for haversine distance"""
        # Test with extreme coordinates
        # North Pole to South Pole (should be ~12450 miles)
        north_pole = (90, 0)
        south_pole = (-90, 0)

        distance = haversine_distance(*north_pole, *south_pole)
        self.assertGreater(distance, 12000)
        self.assertLess(distance, 13000)

    def test_distance_units(self):
        """Test that distance is returned in miles"""
        # London to Paris is approximately 290 miles
        london = (51.5074, -0.1278)
        paris = (48.8566, 2.3522)

        distance = haversine_distance(*london, *paris)
        self.assertGreater(distance, 200)
        self.assertLess(distance, 400)

    def test_mathematical_properties(self):
        """Test mathematical properties of haversine distance"""
        # Triangle inequality (approximate)
        a = (0, 0)
        b = (1, 1)
        c = (2, 2)

        ab = haversine_distance(*a, *b)
        bc = haversine_distance(*b, *c)
        ac = haversine_distance(*a, *c)

        # ac should be less than or equal to ab + bc (with some floating point tolerance)
        self.assertLessEqual(ac, ab + bc + 0.1)


class HomeChoiceValidationTest(TestCase):
    """Test validation of home choices"""

    def test_home_choices_match_constants(self):
        """Test that model choices match constants"""
        from tours.models import TourBooking

        model_choices = dict(TourBooking.HOME_CHOICES)
        constant_keys = set(HOME_LOCATIONS.keys())

        # All model choices should have corresponding constants
        for choice_key in model_choices.keys():
            self.assertIn(choice_key, constant_keys)

        # All constants should have corresponding model choices
        for const_key in constant_keys:
            self.assertIn(const_key, model_choices)

    def test_home_choice_values(self):
        """Test that home choice values are user-friendly"""
        from tours.models import TourBooking

        choices = dict(TourBooking.HOME_CHOICES)

        # Values should be properly capitalized and readable
        for key, value in choices.items():
            self.assertIsInstance(value, str)
            self.assertGreater(len(value), 0)
            # Should not contain underscores in display values
            self.assertNotIn('_', value)

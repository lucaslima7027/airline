from django.test import Client, TestCase
from django.db.models import Max
from flights.models import *

# Create your tests here.

class FlightsTestCase(TestCase):

    def setUp(self):
        #Create some airports
        a1 = Airport.objects.create(code = "AAA", city="City A")
        a2 = Airport.objects.create(code = "BBB", city="City B")

        #Create some flights
        f1 = Flight.objects.create(origin = a1, destination = a2, duration = 100)
        f2 = Flight.objects.create(origin = a1, destination = a1, duration = 100)
        f3 = Flight.objects.create(origin = a1, destination = a2, duration = -100)

    def test_departures_count(self):
        a1 = Airport.objects.get(code="AAA")
        self.assertEqual(a1.departures.count(), 3)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f1 = Flight.objects.get(origin = a1, destination = a2, duration = 100)
        self.assertTrue(f1.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f1 = Flight.objects.get(origin = a1, destination = a2, duration = -100)
        self.assertFalse(f1.is_valid_flight())

    def test_invalid_flight_same_destination(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="AAA")
        f1 = Flight.objects.get(origin = a1, destination = a2, duration = 100)
        self.assertFalse(f1.is_valid_flight())

    #Test flight view
    def test_load_flight_view(self):
        """Index don't loaded"""
        client = Client()
        response = client.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flights'].count(), 3)

    def test_load_flight_detial_view(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f1 = Flight.objects.get(origin = a1, destination = a2, duration = 100)
        client = Client()
        response = client.get(f"/flights/{f1.id}")
        self.assertEqual(response.status_code, 200)

    
    
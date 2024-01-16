from datetime import date, timedelta

from rest_framework import status
from rest_framework.test import APITestCase
from .models import Listing, Assignment

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.listing_1 = Listing.objects.create(first_name="Ross", last_name="Geller")
        self.listing_2 = Listing.objects.create(first_name="Phoebe", last_name="Buffay")
        self.assignment_1 = Assignment.objects.create(
            start_date=date(2023, 2, 7),
            end_date=date(2023, 2, 15),
            listing=self.listing_1,
        )
        self.assignment_2 = Assignment.objects.create(
            start_date=date(2023, 4, 1),
            end_date=date(2023, 4, 4),
            listing=self.listing_2,
        )

class ListingList(BaseAPITestCase):

    def test_get_200(self):
        response = self.client.get("/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_data(self):
        response = self.client.get("/listings/")
        self.assertEqual(
            response.data,
            [
                {
                    "first_name": self.listing_1.first_name,
                    "last_name": self.listing_1.last_name,
                    "pets": [],
                    "assignments": [self.assignment_1.pk],
                },
                {
                    "first_name": self.listing_2.first_name,
                    "last_name": self.listing_2.last_name,
                    "pets": [],
                    "assignments": [self.assignment_2.pk],
                },
            ],
        )


class AssignmentTests(BaseAPITestCase):

    def test_successful_assignment(self):
        data = {
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=5)),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 3)

    def test_assignment_start_date_validation(self):
        data = {
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=5)),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Assignment.objects.count(), 2)


    def test_assignment_overlap_validation(self):
        data = {
            "start_date": str(self.assignment_1.end_date - timedelta(days=1)),
            "end_date": str(self.assignment_1.end_date + timedelta(days=5)),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Assignment.objects.count(), 2)

    def test_required_fields(self):
        data = {}
        response = self.client.post("/listings/assignments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Assignment.objects.count(), 2)

    def test_invalid_listing(self):
        data = {
            "start_date": str(date.today() + timedelta(days=1)),
            "end_date": str(date.today() + timedelta(days=5)),
            "listing": 999,  # Non-existent listing ID
        }
        response = self.client.post("/listings/assignments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Assignment.objects.count(), 2)

    def test_invalid_date_format(self):
        data = {
            "start_date": "invalid_date_format",
            "end_date": str(date.today() + timedelta(days=5)),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Assignment.objects.count(), 2)

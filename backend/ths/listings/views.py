from rest_framework import generics

from .models import Listing, Assignment
from .serializers import ListingSerializer, AssignmentSerializer


class ListingList(generics.ListAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()


class AssignmentCreate(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
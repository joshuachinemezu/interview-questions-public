from rest_framework import serializers

from .models import Listing, Assignment
from datetime import datetime


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["first_name", "last_name", "pets", "assignments"]
        
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["start_date", "end_date", "listing"]

    
    def validate(self, data):
        start_date = data.get("start_date")
        if start_date and start_date <= datetime.now().date():
            raise serializers.ValidationError("Assignment must start tomorrow or later.")

        listing = data.get("listing")
        end_date = data.get("end_date")
        if listing and end_date:
            overlapping_assignments = Assignment.objects.filter(
                listing=listing,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if overlapping_assignments.exists():
                raise serializers.ValidationError("Assignment overlaps with existing assignments.")
            
        # TODO: Additionally, check that end_date is gt or same as the start_date

        return data

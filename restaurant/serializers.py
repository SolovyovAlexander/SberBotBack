from abc import ABC

from rest_framework import serializers, fields


from restaurant.models import Table, Booking


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(BookingSerializer, self).create(validated_data)

    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


class CheckAvailableTablesSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    person_number = serializers.IntegerField()




from datetime import datetime

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from restaurant.models import Booking, Table
from restaurant.serializers import BookingSerializer, TableSerializer, CheckAvailableTablesSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=self.request.user)


class TableViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Table.objects.all()

@swagger_auto_schema(method='POST', request_body=CheckAvailableTablesSerializer)
@api_view(['POST'],)
@authentication_classes([])
def check_availability(request):
    serializer = CheckAvailableTablesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tables = Table.objects.filter(size__gte=serializer.validated_data['person_number']).order_by('size')
    for table in tables:
        if table_is_available(serializer.validated_data['start_time'], serializer.validated_data['end_time'], table.id):
            return Response(
                {"message": "На это время есть подходящие для вас столы", "available": True, "table": table.id,
                 "table_size": table.size})

    return Response({"message": "На это время нет достпуных столов", "available": False})


def table_is_available(start: datetime, end: datetime, table_id):
    table_bookings = Table.objects.get(id=table_id).booking_set.all()
    for booking in table_bookings:
        if booking.reservation_start < start < booking.reservation_end or \
                booking.reservation_start < end < booking.reservation_end or \
                booking.reservation_start >= start and booking.reservation_end <= end:
            return False
    return True

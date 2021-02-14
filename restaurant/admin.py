from django.contrib import admin

from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)


class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class TableAdmin(admin.ModelAdmin):
    search_fields = ('size',)

class BookingAdmin(admin.ModelAdmin):
    search_fields = ('person_name', 'reservation_start', 'reservation_end', 'user', 'table' )


admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Booking, BookingAdmin)

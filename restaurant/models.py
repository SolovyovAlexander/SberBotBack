from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Restaurant(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=256)
    description = models.CharField(verbose_name=_("description"), max_length=256, blank=True)
    opening_time = models.TimeField(verbose_name=_("opening time"))
    closing_time = models.TimeField(verbose_name=_("closing time"))

    def __str__(self):
        return self.name


class Table(models.Model):
    size = models.IntegerField(verbose_name=_("number of persons"), default=2)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE, verbose_name=_("restaurant"))

    def __str__(self):
        return f'{self.restaurant.name} {self.id}'


class User(AbstractUser):

    def __str__(self):
        return f'{self.username}'


class Booking(models.Model):
    table = models.ForeignKey(Table, models.CASCADE, verbose_name=_("table"))
    people = models.IntegerField(verbose_name=_("number of people"))
    reservation_start = models.DateTimeField(verbose_name=_("start of reservation"))
    reservation_end = models.DateTimeField(verbose_name=_("end of reservation"))
    person_name = models.CharField(verbose_name=_("person name"), max_length=256, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'), null=True, blank=True)

    def __str__(self):
        return f'{self.table.restaurant.name} {self.person_name} {self.reservation_start} {self.reservation_end}'

from django.db import models
from django.contrib import admin


class Location(models.Model):
    location_name = models.TextField(null=True, blank = True)

admin.site.register(Location)

class Manufacturer(models.Model):
    manufacturer_name = models.TextField(null=True, blank = True)

admin.site.register(Manufacturer)

class Assets(models.Model):
    location = models.ForeignKey(Location, null=True)
    organization_tag = models.TextField(null=True, blank = True)
    manufacturer = models.ForeignKey(Manufacturer, null=True)
    date = models.DateField(null=True, blank = True)
    part_number = models.TextField(null=True, blank = True)
    desc = models.TextField(null=True, blank=True)
    maintenance_notes = models.TextField(null=True, blank=True)

admin.site.register(Assets)

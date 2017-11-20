from django.db import models
from django.contrib import admin
from django.db import IntegrityError
import random, string
from django.http import  HttpResponse, HttpResponseRedirect

class Location(models.Model):
    location_name = models.TextField(null=True, blank = True)

admin.site.register(Location)

class Manufacturer(models.Model):
    manufacturer_name = models.TextField(null=True, blank = True)

admin.site.register(Manufacturer)

class Assets(models.Model):
    id = models.CharField(primary_key=True, blank=True, unique=True, editable=False, max_length=10)
    location = models.ForeignKey(Location, null=True)
    organization_tag = models.TextField(null=True, blank = True)
    manufacturer = models.ForeignKey(Manufacturer, null=True)
    date = models.DateField(null=True, blank = True)
    part_number = models.TextField(null=True, blank = True)
    description = models.TextField(null=True, blank=True)
    maintenance_notes = models.TextField(null=True, blank=True)

    #overwrite default save function to generate ID & validate uniqueness of ID
    def save(self, *args, **kwargs):
        #if id is not created already, create and insert
        if not self.id:
            print("no id yet")
            self.id = generate_random_alphanumeric(10)
            kwargs['force_insert'] = True

        success = False
        failures = 0

        #loop until success or redirect
        while not success:
            try:
                #try inserting asset
                print("try inserting asset")
                super(Assets, self).save(*args, **kwargs)
            except IntegrityError:
                print("fail")
                #if ID is not unique, add to failure count
                failures += 1

                #after 5 failures, quit because something is wrong and we don't want it to run forver
                if failures > 5:
                    print("failed 5 times")
                    return success
                else:
                    print("try again")
                    #probably just concidence, try again
                    self.id = generate_random_alphanumeric(16)
            else:
                print("success")
                #successfully created unique code, exit loop
                success = True
                return success


admin.site.register(Assets)

def generate_random_alphanumeric(self):
    #create a 10-digit alphanumeric code
    alphanum = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return alphanum

from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect

############### LIST LOCATIONS ###############
@view_function
@login_required(login_url='/index')
def process_request(request):
    '''Lists the locations in a table on the page'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get all locations from DB
    locations = m.Location.objects.all()

    context = {
        'locations': locations,
    }

    return request.dmp_render('locations.html', context)


############### CREATE LOCATION ###############
@view_function
@login_required(login_url='/index')
def create(request):
    '''Creates a new location using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = CreateLocationForm()
    if request.method == 'POST':
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            #create new location
            loc = m.Location()
            loc.location_name = form.cleaned_data.get('name')
            loc.save()

            return HttpResponse('''
            <script>
                window.location.href = '/locations';
            </script>
            ''')

    context = {
        'form': form,
    }
    return request.dmp_render('locations.create.html', context)

class CreateLocationForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


############### EDIT LOCATION ###############
@view_function
@login_required(login_url='/index')
def edit(request):
    '''Edit/Update a preexisting location using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get location by ID
    try:
        loc = m.Location.objects.get(id=request.urlparams[0])
    except m.Location.DoesNotExist:
        return HttpResponseRedirect('/locations')

    #initalize form
    form = EditLocationForm(initial={
        'location_id': loc.id,
        'location_name' : loc.location_name,
    })

    if request.method == 'POST':
        form = EditLocationForm(request.POST)
        if form.is_valid():
            #get location by ID and update fields
            location = m.Location.objects.get(id=request.urlparams[0])
            location.location_name = form.cleaned_data.get('location_name')
            location.save()

            return HttpResponse('''
            <script>
                window.location.href = '/locations';
            </script>
            ''')

    context = {
        'location': loc,
        'form': form,
    }
    return request.dmp_render('locations.edit.html', context)

class EditLocationForm(forms.Form):
    location_id = forms.IntegerField(label='ID', required=False, disabled=True, widget=forms.NumberInput(attrs={ 'class' : "form-control" }))
    location_name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


############### DELETE LOCATION ###############
@view_function
@login_required(login_url='/index')
def delete(request):
    '''Delete a preexisting location from the DB'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get location by ID
    try:
        loc = m.Location.objects.get(id=request.urlparams[0])
    except m.Location.DoesNotExist:
        return HttpResponseRedirect('/locations')

    #delete location
    loc.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/locations';
    </script>
    ''')

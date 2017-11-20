from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect


############### LIST MANUFACTURERS ###############
@view_function
@login_required(login_url='/index')
def process_request(request):
    '''Lists the manufacturers in a table on the page'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get all manufacturers from DB
    manufacturers = m.Manufacturer.objects.all()

    context = {
        'manufacturers': manufacturers,
    }

    return request.dmp_render('manufacturers.html', context)


############### CREATE MANUFACTURER ###############
@view_function
@login_required(login_url='/index')
def create(request):
    '''Creates a new manufacturer using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = CreateManufacturerForm()
    if request.method == 'POST':
        form = CreateManufacturerForm(request.POST)
        if form.is_valid():
            #create new manufacturer
            manu = m.Manufacturer()
            manu.manufacturer_name = form.cleaned_data.get('name')
            manu.save()

            return HttpResponse('''
            <script>
                window.location.href = '/manufacturers';
            </script>
            ''')

    context = {
        'form': form,
    }
    return request.dmp_render('manufacturers.create.html', context)

class CreateManufacturerForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


############### EDIT MANUFACTURER ###############
@view_function
@login_required(login_url='/index')
def edit(request):
    '''Edit/Update a preexisting manufacturer using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get manufacturer by ID
    try:
        manu = m.Manufacturer.objects.get(id=request.urlparams[0])
    except m.Manufacturer.DoesNotExist:
        return HttpResponseRedirect('/manufacturers')

    #intialize form
    form = EditManufacturerForm(initial={
        'manufacturer_id': manu.id,
        'manufacturer_name' : manu.manufacturer_name,
    })

    if request.method == 'POST':
        form = EditManufacturerForm(request.POST)
        if form.is_valid():
            #get manufacturer by ID and update fields
            manufacturer = m.Manufacturer.objects.get(id=request.urlparams[0])
            manufacturer.manufacturer_name = form.cleaned_data.get('manufacturer_name')
            manufacturer.save()

            return HttpResponse('''
            <script>
                window.location.href = '/manufacturers';
            </script>
            ''')

    context = {
        'manufacturer': manu,
        'form': form,
    }
    return request.dmp_render('manufacturers.edit.html', context)

class EditManufacturerForm(forms.Form):
    manufacturer_id = forms.IntegerField(label='ID', required=False, disabled=True, widget=forms.NumberInput(attrs={ 'class' : "form-control" }))
    manufacturer_name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


############### DELETE MANUFACTURER ###############
@view_function
@login_required(login_url='/index')
def delete(request):
    '''Delete a preexisting manufacturer from DB'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get manufacturer by ID
    try:
        manu = m.Manufacturer.objects.get(id=request.urlparams[0])
    except m.Manufacturer.DoesNotExist:
        return HttpResponseRedirect('/manufacturers')

    #delete manufacturer
    manu.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/manufacturers';
    </script>
    ''')

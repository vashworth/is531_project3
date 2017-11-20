from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect
import datetime

############### LIST ASSETS ###############
@view_function
@login_required(login_url='/index')
def process_request(request):
    '''Lists the assets in a table on the page'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get all assets, location, manufacturers from DB
    assets = m.Assets.objects.all()
    locations = m.Location.objects.all()
    manufacturers = m.Manufacturer.objects.all()

    context = {
        'assets': assets,
        'locations' : locations,
        'manufacturers' : manufacturers,
    }

    return request.dmp_render('assets.html', context)


############### CREATE ASSET ###############
@view_function
@login_required(login_url='/index')
def create(request):
    '''Creates a new asset using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = CreateAssetForm()
    if request.method == 'POST':
        form = CreateAssetForm(request.POST)
        if form.is_valid():
            #create new asset
            a = m.Assets()
            a.description = form.cleaned_data.get('desc')
            a.organization_tag = form.cleaned_data.get('organization_tag')
            a.location_id = form.cleaned_data.get('location_id')
            a.manufacturer_id = form.cleaned_data.get('manufacturer_id')
            a.part_number = form.cleaned_data.get('part_number')
            a.maintenance_notes = form.cleaned_data.get('maintenance_notes')
            a.date = datetime.datetime.today().strftime('%Y-%m-%d')
            success = a.save()

            if success is True:
                return HttpResponse('''
                <script>
                    window.location.href = '/assets';
                </script>
                ''')
            else:
                return HttpResponse('''
                <script>
                    alert("An error occured. Please try again later.")
                    window.location.href = '/assets';
                </script>
                ''')


    context = {
        'form': form,
    }
    return request.dmp_render('assets.create.html', context)

class CreateAssetForm(forms.Form):
    desc = forms.CharField(label='Description', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    organization_tag = forms.CharField(label='Organization Tag', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    location_id = forms.ChoiceField(label='Location', choices=[], required=True, widget=forms.Select(attrs={ 'class' : "form-control" }))
    manufacturer_id = forms.ChoiceField(label='Manufacturer', choices=[], required=True, widget=forms.Select(attrs={ 'class' : "form-control" }))
    part_number = forms.CharField(label='Manufacturer Part Number', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    maintenance_notes = forms.CharField(label='Maintenance Notes', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    date = forms.CharField(label='Date Implemented', required=True, max_length=100, widget=forms.TextInput(attrs={ 'id' : "datepicker", 'class' : "form-control" }))

    def __init__(self, *args, **kwargs):
        super(CreateAssetForm, self).__init__(*args, **kwargs)
        self.fields['location_id'].choices = [(x.pk, x.location_name) for x in m.Location.objects.all().order_by('location_name')]
        self.fields['manufacturer_id'].choices = [(x.pk, x.manufacturer_name) for x in m.Manufacturer.objects.all().order_by('manufacturer_name')]


############### EDIT ASSET ###############
@view_function
@login_required(login_url='/index')
def edit(request):
    '''Edits/Updates a preexisting asset using a form'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get asset by id
    try:
        asset = m.Assets.objects.get(id=request.urlparams[0])
    except m.Assets.DoesNotExist:
        return HttpResponseRedirect('/assets')

    #initalize form
    form = EditAssetForm(initial={
        'asset_id': asset.id,
        'desc': asset.description,
        'organization_tag': asset.organization_tag,
        'location_id': asset.location,
        'manufacturer_id': asset.manufacturer,
        'part_number': asset.part_number,
        'maintenance_notes': asset.maintenance_notes,
        'date': asset.date,
    })

    if request.method == 'POST':
        form = EditAssetForm(request.POST)
        if form.is_valid():
            #get asset by id and update values
            a = m.Assets.objects.get(id=request.urlparams[0])
            a.description = form.cleaned_data.get('desc')
            a.organization_tag = form.cleaned_data.get('organization_tag')
            a.location_id = form.cleaned_data.get('location_id')
            a.manufacturer_id = form.cleaned_data.get('manufacturer_id')
            a.part_number = form.cleaned_data.get('part_number')
            a.maintenance_notes = form.cleaned_data.get('maintenance_notes')
            a.date = datetime.datetime.today().strftime('%Y-%m-%d')
            a.save()

            return HttpResponseRedirect('/assets')

    context = {
        'asset': asset,
        'form': form,
    }
    return request.dmp_render('assets.edit.html', context)

class EditAssetForm(forms.Form):
    asset_id = forms.CharField(label='ID', required=False, disabled=True, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    desc = forms.CharField(label='Description', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    organization_tag = forms.CharField(label='Organization Tag', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    location_id = forms.ChoiceField(label='Location', choices=[], required=True, widget=forms.Select(attrs={ 'class' : "form-control" }))
    manufacturer_id = forms.ChoiceField(label='Manufacturer', choices=[], required=True, widget=forms.Select(attrs={ 'class' : "form-control" }))
    part_number = forms.CharField(label='Manufacturer Part Number', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    maintenance_notes = forms.CharField(label='Maintenance Notes', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    date = forms.CharField(label='Date Implemented', required=True, max_length=100, widget=forms.TextInput(attrs={ 'id' : "datepicker", 'class' : "form-control" }))

    def __init__(self, *args, **kwargs):
        super(EditAssetForm, self).__init__(*args, **kwargs)
        self.fields['location_id'].choices = [(x.pk, x.location_name) for x in m.Location.objects.all().order_by('location_name')]
        self.fields['manufacturer_id'].choices = [(x.pk, x.manufacturer_name) for x in m.Manufacturer.objects.all().order_by('manufacturer_name')]

############### DELETE ASSET ###############
@view_function
@login_required(login_url='/index')
def delete(request):
    '''Deletes a preexisting asset from DB'''

    #require login
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    #get asset
    try:
        asset = m.Assets.objects.get(id=request.urlparams[0])
    except m.Assets.DoesNotExist:
        return HttpResponseRedirect('/assets')

    #delete asset
    asset.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/assets';
    </script>
    ''')

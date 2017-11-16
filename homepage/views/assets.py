from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect
import datetime


@view_function
@login_required(login_url='/index')
def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    assets = m.Assets.objects.all()
    locations = m.Location.objects.all()
    manufacturers = m.Manufacturer.objects.all()

    template_vars = {
        'assets': assets,
        'locations' : locations,
        'manufacturers' : manufacturers,
    }

    return request.dmp_render('assets.html', template_vars)

@view_function
@login_required(login_url='/index')
def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    print( datetime.datetime.today().strftime('%Y-%m-%d') )


    form = CreateAssetForm()
    if request.method == 'POST':
        form = CreateAssetForm(request.POST)
        if form.is_valid():
            a = m.Assets()
            a.desc = form.cleaned_data.get('desc')
            a.organization_tag = form.cleaned_data.get('organization_tag')
            a.location_id = form.cleaned_data.get('location_id')
            a.manufacturer_id = form.cleaned_data.get('manufacturer_id')
            a.part_number = form.cleaned_data.get('part_number')
            a.maintenance_notes = form.cleaned_data.get('maintenance_notes')
            a.date = datetime.datetime.today().strftime('%Y-%m-%d')
            a.save()

            return HttpResponse('''
            <script>
                window.location.href = '/assets';
            </script>
            ''')

    template_vars = {
        'form': form,
    }
    return request.dmp_render('assets.create.html', template_vars)

class CreateAssetForm(forms.Form):
    desc = forms.CharField(label='Description', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    organization_tag = forms.CharField(label='Organization Tag', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    location_id = forms.ChoiceField(label='Location', choices=[], required=True, widget=forms.Select(attrs={ 'class' : "form-control" }))
    manufacturer_id = forms.ChoiceField(label='Manufacturer', choices=[], required=True, widget=forms.Select(attrs={ 'class' : "form-control" }))
    part_number = forms.CharField(label='Manufacturer Part Number', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    maintenance_notes = forms.CharField(label='Maintenance Notes', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))
    date = forms.CharField(label='Date Implemented', required=True, max_length=100, widget=forms.TextInput(attrs={ 'placeholder' : "YYYY-MM-DD", 'class' : "form-control" }))

    def __init__(self, *args, **kwargs):
        super(CreateAssetForm, self).__init__(*args, **kwargs)
        self.fields['location_id'].choices = [(x.pk, x.location_name) for x in m.Location.objects.all().order_by('location_name')]
        self.fields['manufacturer_id'].choices = [(x.pk, x.manufacturer_name) for x in m.Manufacturer.objects.all().order_by('manufacturer_name')]

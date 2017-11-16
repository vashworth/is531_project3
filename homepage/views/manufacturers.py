from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from homepage import models as m
from django import forms
from django.http import  HttpResponse, HttpResponseRedirect

@view_function
@login_required(login_url='/index')
def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    manufacturers = m.Manufacturer.objects.all()

    template_vars = {
        'manufacturers': manufacturers,
    }

    return request.dmp_render('manufacturers.html', template_vars)

@view_function
@login_required(login_url='/index')
def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = CreateManufacturerForm()
    if request.method == 'POST':
        form = CreateManufacturerForm(request.POST)
        if form.is_valid():
            loc = m.Manufacturer()
            loc.manufacturer_name = form.cleaned_data.get('name')
            loc.save()

            return HttpResponse('''
            <script>
                window.location.href = '/manufacturers';
            </script>
            ''')

    template_vars = {
        'form': form,
    }
    return request.dmp_render('manufacturers.create.html', template_vars)

class CreateManufacturerForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))



@view_function
@login_required(login_url='/index')
def edit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    try:
        loc = m.Manufacturer.objects.get(id=request.urlparams[0])
    except m.Manufacturer.DoesNotExist:
        return HttpResponseRedirect('/manufacturers')

    form = EditManufacturerForm(initial={
        'manufacturer_id': loc.id,
        'manufacturer_name' : loc.manufacturer_name,
    })

    if request.method == 'POST':
        form = EditManufacturerForm(request.POST)
        if form.is_valid():
            manufacturer = m.Manufacturer.objects.get(id=request.urlparams[0])
            manufacturer.manufacturer_name = form.cleaned_data.get('manufacturer_name')
            manufacturer.save()

            return HttpResponse('''
            <script>
                window.location.href = '/manufacturers';
            </script>
            ''')

    template_vars = {
        'manufacturer': loc,
        'form': form,
    }
    return request.dmp_render('manufacturers.edit.html', template_vars)

class EditManufacturerForm(forms.Form):
    manufacturer_id = forms.IntegerField(label='ID', required=False, disabled=True, widget=forms.NumberInput(attrs={ 'class' : "form-control" }))
    manufacturer_name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


@view_function
@login_required(login_url='/index')
def delete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    try:
        loc = m.Manufacturer.objects.get(id=request.urlparams[0])
    except m.Manufacturer.DoesNotExist:
        return HttpResponseRedirect('/manufacturers')

    loc.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/manufacturers';
    </script>
    ''')

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

    locations = m.Location.objects.all()

    template_vars = {
        'locations': locations,
    }

    return request.dmp_render('locations.html', template_vars)

@view_function
@login_required(login_url='/index')
def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    form = CreateLocationForm()
    if request.method == 'POST':
        form = CreateLocationForm(request.POST)
        if form.is_valid():
            loc = m.Location()
            loc.location_name = form.cleaned_data.get('name')
            loc.save()

            return HttpResponse('''
            <script>
                window.location.href = '/locations';
            </script>
            ''')

    template_vars = {
        'form': form,
    }
    return request.dmp_render('locations.create.html', template_vars)

class CreateLocationForm(forms.Form):
    name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))



@view_function
@login_required(login_url='/index')
def edit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    try:
        loc = m.Location.objects.get(id=request.urlparams[0])
    except m.Location.DoesNotExist:
        return HttpResponseRedirect('/locations')

    form = EditLocationForm(initial={
        'location_id': loc.id,
        'location_name' : loc.location_name,
    })

    if request.method == 'POST':
        form = EditLocationForm(request.POST)
        if form.is_valid():
            location = m.Location.objects.get(id=request.urlparams[0])
            location.location_name = form.cleaned_data.get('location_name')
            location.save()

            return HttpResponse('''
            <script>
                window.location.href = '/locations';
            </script>
            ''')

    template_vars = {
        'location': loc,
        'form': form,
    }
    return request.dmp_render('locations.edit.html', template_vars)

class EditLocationForm(forms.Form):
    location_id = forms.IntegerField(label='ID', required=False, disabled=True, widget=forms.NumberInput(attrs={ 'class' : "form-control" }))
    location_name = forms.CharField(label='Name', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class' : "form-control" }))


@view_function
@login_required(login_url='/index')
def delete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    try:
        loc = m.Location.objects.get(id=request.urlparams[0])
    except m.Location.DoesNotExist:
        return HttpResponseRedirect('/locations')

    loc.delete()

    return HttpResponse('''
    <script>
        window.location.href = '/locations';
    </script>
    ''')

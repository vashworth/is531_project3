from django_mako_plus import view_function
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    # log the user out
    logout(request)

    return HttpResponseRedirect('/index')

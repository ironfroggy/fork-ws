# Create your views here.

from json import dumps

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from forkws.models import Fork
from forkws.forms import ForkForm

# API

def json_view(f):
    return lambda *a, **k: dumps(f(*a, **k))

@json_view
def new(request):
    fork = Fork(body = request.POST)
    return {'result': str(fork.id)}

@json_view
def fork(request, parent_id):
    parent = Fork.objects.get(id=int(parent_id))
    child = parent.fork(body=request.POST, parent=parent)
    return {'result': str(fork.id)}

@json_view
def merge(request, to_id, from_id):
    to_fork = Fork.objects.get(id=int(to_id))
    from_fork = Fork.objects.get(id=int(from_id))

    to_fork.merge(from_fork)

    return {'dirty': to_fork.dirty}


# CRUD

def new_page(request):
    if request.POST:
        form = ForkForm(request.POST)
        if form.is_valid():
            fork = form.save()
            return HttpResponseRedirect(reverse('view_fork', kwargs={'id': fork.id}))
    else:
        form = ForkForm()
    return render_to_response("forkws/new.html", locals())

def view_fork(request, id):
    fork = Fork.objects.get(id=id)
    form = ForkForm(instance=fork)
    return render_to_response("forkws/new.html", locals())

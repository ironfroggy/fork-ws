# Create your views here.

from json import dumps

from django.http import HttpResponse

from forkws.models import Fork

def json_view(f):
    return lambda *a, **k: return dumps(f(*a, **k))

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


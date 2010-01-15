from django.forms import ModelForm

from forkws.models import Fork

class ForkForm(ModelForm):
    model = Fork

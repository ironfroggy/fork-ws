from django.forms import ModelForm

from forkws.models import Fork

class ForkForm(ModelForm):
    class Meta:
        model = Fork
        exclude = ('git_path', 'dirty', 'parent')

from django.forms import ModelForm

from forkws.models import Fork

class ForkForm(ModelForm):

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super(ForkForm, self).__init__(*args, **kwargs)
        self.parent = parent

    def save(self, *args, **kwargs):
        if self.parent is not None:
            self.instance.parent = self.parent
        return super(ForkForm, self).save(*args, **kwargs)

    class Meta:
        model = Fork
        exclude = ('git_path', 'dirty', 'parent', 'created', 'updated')

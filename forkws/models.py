import os
from tempfile import mkdtemp

from django.db import models
from django.conf import settings

from git.cmd import Git

class Fork(models.Model):
    """Represents one body of text that is and can be forked."""

    git_path = models.FilePathField(settings.GIT_ROOT_PATH)
    parent = models.ForeignKey('self', blank=True, null=True)
    body = models.TextField(null=False, blank=False)

    def __init__(self, **kwargs):
        if not kwargs.get('parent', None):
            # Initialize a new repo
            if not os.path.exists(settings.GIT_ROOT_PATH):
                os.mkdir(settings.GIT_ROOT_PATH)
            git_path = mkdtemp(prefix=settings.GIT_ROOT_PATH)
            git = Git(git_path)
            git.init()

            body_path = os.path.join(git_path, 'BODY')
            print >>open(body_path, 'w'), kwargs['body']

            git.add(body_path)
            git.commit(message="created new")

        super(Fork, self).__init__(**kwargs)

    def fork(self, new_body):
        pass 

import os
from tempfile import mkdtemp

from django.db import models
from django.conf import settings

from git.cmd import Git, GitCommandError
from git.repo import Repo

if not os.path.exists(settings.GIT_ROOT_PATH):
    os.mkdir(settings.GIT_ROOT_PATH)

class Fork(models.Model):
    """Represents one body of text that is and can be forked."""

    git_path = models.FilePathField(settings.GIT_ROOT_PATH)
    parent = models.ForeignKey('self', blank=True, null=True)
    body = models.TextField(null=False, blank=False)
    dirty = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('parent', None):
            # Initialize a new repo
            git_path = mkdtemp(prefix=settings.GIT_ROOT_PATH)
            git = Git(git_path)
            git.init()

            body_path = os.path.join(git_path, 'BODY')

            self.message = "created new"

            kwargs['git_path'] = git_path

        super(Fork, self).__init__(*args, **kwargs)

    def _next_message(self):
        message = self.message
        self.message = None
        return message

    def save(self, *args, **kwargs):
        message = kwargs.pop('message', self._next_message() or 'update')

        super(Fork, self).save(*args, **kwargs)
        with open(os.path.join(self.git_path, "BODY"), 'w') as f:
            f.write(self.body)
        git = Git(self.git_path)
        git.add('BODY')

        try:
            git.commit(message=message)
        except GitCommandError, e:
            if e.status != 1:
                raise

    def _reload_body(self):
        self.body = open(os.path.join(self.git_path, "BODY")).read()
        self.save()

    def fork(self, new_body):
        git_path = mkdtemp(prefix=settings.GIT_ROOT_PATH)
        git = Git(git_path)
        git.clone(os.path.abspath(self.git_path), git_path)

        new_fork = Fork.objects.create(body=new_body, parent=self, git_path=git_path)
        return new_fork

    def _forward(self, forward_fork):
        git = Git(self.git_path)
        git.pull(forward_fork.git_path, 'master')
        self._reload_body()

    def merge(self, child_fork):
        try:
            self._forward(child_fork)
        except GitCommandError, e:
            if e.status == 1:
                self._reload_body()
                self.dirty = True
                self.save()
            else:
                raise

    def resolve(self, resolution):
        self.body = resolution
        self.dirty = False
        self.save()

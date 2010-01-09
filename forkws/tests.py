"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import os

from django.test import TestCase

from forkws.models import Fork

class ForkingTest(TestCase):

    def test_new(self):
        f = Fork.objects.create(body="0123456789")
        self.failUnlessEqual("0123456789", f.body)

    def test_new_git(self):
        f = Fork.objects.create(body="0123456789")
        f.git_path

    def test_fork(self):
        """I'm not sure how to write good tests for this."""
        f1 = Fork.objects.create(body="0123456789")
        f2 = f1.fork("0123456789\nabcdefghij")
        self.failUnlessEqual(f1, f2.parent)
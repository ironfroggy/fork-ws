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
        f1 = Fork.objects.create(body="0123456789")
        f2 = f1.fork("0123456789\nabcdefghij")
        self.failUnlessEqual(f1, f2.parent)

        self.failUnlessEqual(f2.body, "0123456789\nabcdefghij") 

    def test_forward(self):
        f1 = Fork.objects.create(body="0123456789")
        f2 = f1.fork("0123456789\nabcdefghij")

        f1._forward(f2)

        self.failUnlessEqual(f1.body, "0123456789\nabcdefghij") 

    def test_merge_conflict(self):
        f1 = Fork.objects.create(body="0123456789")
        f2 = f1.fork("0123456789\nabcdefghij")
        f3 = f1.fork("0123456789\nklmnopqrst")

        f2.merge(f3)

        self.failIfEqual(f2.body, "0123456789\nabcdefghij")
        assert f2.dirty

    def test_resolve(self):
        f1 = Fork.objects.create(body="0123456789")
        f2 = f1.fork("0123456789\nabcdefghij")
        f3 = f1.fork("0123456789\nklmnopqrst")

        f2.merge(f3)

        f2.resolve("0123456789\nklmnopqrst")
        resolved_body = open(os.path.join(f2.git_path, 'BODY')).read()
        assert resolved_body == "0123456789\nklmnopqrst"


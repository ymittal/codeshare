from __future__ import unicode_literals

from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class CodeSnippet(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(null=True,
                             max_length=30,
                             blank=True)
    code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title + " | " + str(self.timestamp)

    def __str__(self):
        return self.title + " | " + str(self.timestamp)

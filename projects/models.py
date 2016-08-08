from __future__ import unicode_literals

import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from clients.models import Client


class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client)
    cost_per_hour = models.FloatField(blank=False, default=1)
    total_cost = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectTimeline(models.Model):
    project = models.ForeignKey(Project)
    time_spent = models.FloatField(blank=False, null=False, max_length=2,
        validators=[
            MaxValueValidator(24),
            MinValueValidator(0)
        ])
    # By Default it'll take spent on as current date
    spent_on = models.DateField(blank=True, null=True, default=datetime.date.today())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if self.project.completed:
            raise ValidationError('Trying to Add Timeline to the complted project')
        elif self.time_spent > 24 or self.time_spent < 0:
            print 'Time must be 0 to 24'
        else:
            super(ProjectTimeline, self).save(*args, **kwargs)

    def __str__(self):
        return self.project.name
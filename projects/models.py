from __future__ import unicode_literals

import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from clients.models import Client


class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client)
    cost_per_hour = models.FloatField(blank=False, default=1)
    # expense is cost_per_hour * hour_spent
    expense = models.FloatField(blank=True, null=True, default=0)
    start_date = models.DateField(blank=True, null=True)
    expected_end_date = models.DateField(blank=True, null=True)
    # summation of all project spent hours
    total_hours_spent = models.IntegerField(blank=True, default=0)
    end_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Project, self).save()
        projects = Project.objects.filter(client=self.client)
        total_income = 0
        for project in projects:
            total_income += project.expense

        self.client.total_income = total_income
        self.client.save()


class ProjectTimeline(models.Model):
    project = models.ForeignKey(Project)
    time_spent = models.IntegerField(blank=False, null=False,
                                     validators=[
                                         MaxValueValidator(24),
                                         MinValueValidator(1)
                                     ])
    # By Default it'll take spent on as current date
    spent_on = models.DateField(blank=False, null=False, default=datetime.date.today())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(ProjectTimeline, self).save()
        expense = self.project.cost_per_hour * self.time_spent
        self.project.expense += expense
        self.project.total_hours_spent += self.time_spent
        self.project.save()

    def delete(self, using=None, keep_parents=False):
        # Subtract the expense when delete
        expense = self.project.cost_per_hour * self.time_spent
        self.project.expense -= expense
        self.project.total_hours_spent -= self.time_spent
        self.project.save()
        super(ProjectTimeline, self).delete()


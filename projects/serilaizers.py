from rest_framework import serializers
from projects.models import Project, ProjectTimeline


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'cost_per_hour', 'completed', 'created_at',
                  'client', 'start_date', 'end_date', 'expense', 'total_hours_spent' )


class ProjectTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTimeline
        fields = ('id', 'project', 'time_spent', 'spent_on', 'created_at')



from rest_framework import serializers
from projects.models import Project, ProjectTimeline


class ProjectSerializer(serializers.ModelSerializer):
    total_hours_spent = serializers.IntegerField(read_only=True)
    expense = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    cost_per_hour = serializers.FloatField(allow_null=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'cost_per_hour', 'completed', 'created_at',
                  'client', 'start_date', 'end_date', 'expense', 'total_hours_spent')


class ProjectTimelineSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProjectTimeline
        fields = ('id', 'project', 'time_spent', 'spent_on', 'created_at')



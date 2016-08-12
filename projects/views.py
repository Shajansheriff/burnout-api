from django.core import serializers
from rest_framework.response import Response
from clients.models import Client
from projects.models import Project, ProjectTimeline
from projects.serilaizers import ProjectSerializer, ProjectTimelineSerializer
from django.http import Http404
from rest_framework import viewsets, generics, status


class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD Project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        if request.GET.get('client'):
            try:
                client = Client.objects.get(pk=request.GET.get('client'))
            except Client.DoesNotExist:
                raise Http404
            else:
                projects = self.queryset.filter(client=client)
                serializer = ProjectSerializer(projects, many=True)
                return Response(serializer.data)
        else:
            return Response(ProjectSerializer(self.queryset, many=True).data)

    def update(self, request, pk, *args, **kwargs):
        project_serializers = ProjectSerializer(data=request.data)
        if project_serializers.is_valid():
            new_cost_per_hour = project_serializers.data.get('cost_per_hour')
            client = project_serializers.data.get('client')
            try:
                project = Project.objects.get(pk=pk)
            except Client.DoesNotExist:
                raise Http404
            # getting the current total hours spent in the project
            total_hours_spent = project.total_hours_spent
            # Calculating new expense
            new_expense = total_hours_spent * new_cost_per_hour
            project.expense = new_expense
            project.cost_per_hour = new_cost_per_hour
            project.save()
            return Response(project_serializers.data, status=201)
        else:
            return Response(project_serializers.errors, status=400)


class ClientProjectList(generics.ListAPIView):
    """
    return the list of projects of a client
    """
    model = Project
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super(ClientProjectList, self).get_queryset()
        return queryset.filter(client=self.kwargs.get('client'))


class ClientProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Method Allowed: GET, PUT, DESTROY
    UPDATE, DELETE Project of a client
    """
    model = Project
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer

    # Return the Client Object
    # Params: Project primary key
    def get_object(self, pk=None):

        try:
            return Project.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queryset = super(ClientProjectDetail, self).get_queryset()
        return queryset.filter(client=self.kwargs.get('client'))

    def update(self, request, pk, *args, **kwargs):
        project_serializers = ProjectSerializer(data=request.data)
        if project_serializers.is_valid():
            new_cost_per_hour = project_serializers.data.get('cost_per_hour')
            client = project_serializers.data.get('client')
            project = self.get_object(pk=pk)
            # getting the current total hours spent in the project
            total_hours_spent = project.total_hours_spent
            #  Calculating new expense
            new_expense = total_hours_spent * new_cost_per_hour
            project.expense = new_expense
            project.cost_per_hour = new_cost_per_hour
            project.save()
            return Response(project_serializers.data, status=201)
        else:
            return Response(project_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectTimelineList(generics.ListAPIView):
    """
    Method Allowed: GET
    List ProjectTimeline by Project
    """
    model = Project
    queryset = ProjectTimeline.objects.all()

    serializer_class = ProjectTimelineSerializer

    def get_queryset(self):
        queryset = super(ProjectTimelineList, self).get_queryset()
        return queryset.filter(project=self.kwargs.get('project'))


class ProjectTimelineCreate(generics.CreateAPIView):
    """
    Method Allowed: POST
    Create a new timeline for the project
    """
    model = ProjectTimeline
    queryset = ProjectTimeline.objects.all()
    serializer_class = ProjectTimelineSerializer


class ProjectTimelineViewSet(viewsets.ModelViewSet):
    """
    CRUD Project-Timeline
    """
    model = ProjectTimeline
    queryset = ProjectTimeline.objects.all()
    serializer_class = ProjectTimelineSerializer

    def create(self, request, *args, **kwargs):
        print  request.POST.get('spent_on')
        timeline_list = ProjectTimeline.objects.filter(project=request.POST.get('project'),
                                                       spent_on=request.POST.get('spent_on'))
        if timeline_list:
            total_time = int(0)
            for time in timeline_list:
                total_time += int(time.time_spent)

            total_time += int(request.POST.get('time_spent'))
            if total_time > 24:
                return Response({'error: Time Spent on the Date is High'}, status=400)

        serializer = ProjectTimelineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

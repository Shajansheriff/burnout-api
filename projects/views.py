from rest_framework.response import Response
from clients.models import Client
from projects.models import Project, ProjectTimeline
from projects.serilaizers import ProjectSerializer, ProjectTimelineSerializer
from django.http import Http404
from rest_framework import viewsets, generics


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
    UPDATE, DELETE Project of a client
    """
    model = Project
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super(ClientProjectDetail, self).get_queryset()
        return queryset.filter(client=self.kwargs.get('client'))


class ProjectTimelineList(generics.ListAPIView):
    """
    List ProjectTimeline
    """
    model = Project
    queryset = ProjectTimeline.objects.all()
    serializer_class = ProjectTimelineSerializer

    def get_queryset(self):
        queryset = super(ProjectTimelineList, self).get_queryset()
        return queryset.filter(project=self.kwargs.get('project'))


class ProjectTimelineViewSet(viewsets.ModelViewSet):
    queryset = ProjectTimeline.objects.all()
    serializer_class = ProjectTimelineSerializer



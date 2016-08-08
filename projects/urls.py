from django.conf.urls import url
from projects.views import ProjectViewSet, ClientProjectList, ProjectTimelineViewSet, ProjectTimelineList
from rest_framework import routers


urlpatterns = [
    #url(r'^projects/(?P<pk>[0-9]+)/project-timeline$', ProjectTimelineList.as_view(), name="project_detail"),
    url(r'^clients/(?P<client>[0-9]+)/projects/$', ClientProjectList.as_view(), name="client_project_list"),
    url(r'^projects/(?P<project>[0-9]+)/timeline/$', ProjectTimelineList.as_view(), name="project_timeline_list")
]
router = routers.DefaultRouter()
router.register(r'project-timeline', ProjectTimelineViewSet, 'projects_timeline')
router.register(r'projects', ProjectViewSet, 'projects_list')
urlpatterns += router.urls
from django.conf.urls import url
from projects.views import ProjectViewSet, ClientProjectList, \
    ProjectTimelineViewSet, ProjectTimelineList, ClientProjectDetail
from rest_framework import routers

urlpatterns = [
    url(r'^clients/(?P<client>[0-9]+)/projects/$', ClientProjectList.as_view(), name="client_project_list"),
    url(r'^clients/(?P<client>[0-9]+)/projects/(?P<pk>[0-9]+)/$', ClientProjectDetail.as_view(),
        name="client_project_list"),
    url(r'^projects/(?P<project>[0-9]+)/timeline/$', ProjectTimelineList.as_view(), name="project_timeline_list")
]
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, 'projects_list')
router.register(r'project-timeline', ProjectTimelineViewSet, 'projects_timeline')
urlpatterns += router.urls

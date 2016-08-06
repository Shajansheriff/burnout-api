from django.conf.urls import url
from clients.views import ClientList, ClientDetail


urlpatterns = [
    url(r'^$', ClientList.as_view(), name="client_list"),
    url(r'^(?P<pk>[0-9]+)/$', ClientDetail.as_view(), name="client_detail")
]
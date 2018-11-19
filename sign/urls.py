from django.conf.urls import  url
from sign import views_if

urlpatterns = [
    # ex : /api/add_event/
    url(r'^add_event/',views_if.add_event,name='add_event'),
]
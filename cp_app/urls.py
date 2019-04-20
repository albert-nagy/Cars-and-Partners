from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root, name="index"),
    url(r'^partners/$', views.partner_list),
    url(r'^partners/(\d+)/', views.partner_detail),
]
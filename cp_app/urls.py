from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root, name="index"),
    url(r'^add_user$', views.UserAdd.as_view()),
    url(r'^partners/$', views.PartnerList.as_view()),
    url(r'^partners/(\d+)$', views.PartnerDetail.as_view()),
]
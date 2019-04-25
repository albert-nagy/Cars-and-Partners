from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^add_user/$', views.UserAdd.as_view(), name="add-user"),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^partners/$', views.PartnerList.as_view(), name="partner-list"),
    url(r'^partners/(\d+)/$', views.PartnerDetail.as_view(), name="partner"),
    url(r'^cars/$', views.CarList.as_view(), name="car-list"),
    url(r'^cars/(\d+)/$', views.CarDetail.as_view(), name="car"),
]

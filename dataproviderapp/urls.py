from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'register',views.RegisterUserViewSet)
router.register(r'country',views.CountryViewSet)
router.register(r'state',views.StateViewSet)
router.register(r'city',views.CityViewSet)
router.register(r'properties',views.PropertyViewSet)
router.register(r'propertytype',views.PropertyTypeViewSet)
router.register(r'propertystatus',views.PropertyStatusViewSet)
router.register(r'propertypurpose',views.PropertyPurposeViewSet)
router.register(r'userprofile',views.UserProfileViewSet)
urlpatterns = [
  url(r'^admin/', admin.site.urls),
  path('',views.index,name='index'),
  path('', include(router.urls)),
  path(r'api-token-auth/', obtain_jwt_token),
  path(r'api-token-refresh/', refresh_jwt_token),
  path(r'current_user/',views.current_user),
  path(r'set_user_status/<int:userid>',views.set_user_status),
  path(r'recommend/',views.recommend),
  path(r'predictSalePrice/',views.predictSalePrice),
  path(r'chartdata/',views.chartdata),
  path(r'property/',views.PropertyFilterViewSet.as_view()),
  path(r'propertyforuser/',views.PropertyBasedOnUserViewSet.as_view()),
  #path(r'userprofile/',views.UserProfileViewSet.as_view()),
  #predictSalePrice
]


from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'main'
router = routers.DefaultRouter()
router.register(r'components', ComponentViewset)
router.register(r'records', RecordViewset)
router.register(r'types', TypeViewset)
router.register(r'attrs', AttrViewset)

urlpatterns = [
    path(r'', include(router.urls)),
]

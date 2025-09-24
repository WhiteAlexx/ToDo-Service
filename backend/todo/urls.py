from django.urls import path, include

from rest_framework.routers import DefaultRouter

from todo import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]

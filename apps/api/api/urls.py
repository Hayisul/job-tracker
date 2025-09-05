"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import ApplicationViewSet, ContactViewSet, TaskViewSet

# Top-level router
router = DefaultRouter()
router.register(r"applications", ApplicationViewSet, basename="application")

# Nested routers under /api/applications/{application_pk}/...
nested = NestedDefaultRouter(router, r"applications", lookup="application")
nested.register(r"contacts", ContactViewSet, basename="application-contacts")
nested.register(r"tasks", TaskViewSet, basename="application-tasks")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),  # /api/applications/
    path("api/", include(nested.urls)),  # /api/applications/{id}/contacts/, /tasks/
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

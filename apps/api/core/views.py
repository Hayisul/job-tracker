from rest_framework import viewsets, permissions
from django.db.models import Prefetch
from .models import Application, Contact, Task
from .serializers import ApplicationSerializer


class IsOwner(permissions.BasePermission):
    """
    Object-level permission thst ensures the requesting user owns the resource.
    Works for:
    - Models with a `user` field (Application)
    - Models with an `application` FK that itself has a `user` (Contact, Task)
    """

    def has_object_permission(self, request, view, obj):
        # Try direct owner (e.g., Application.user)
        owner = getattr(obj, "user", None)
        if owner is not None:
            return owner == request.user

        # Fallback: owner via related Application (e.g., Contact.application.user)
        application = getattr(obj, "application", None)
        if application is not None:
            return application.user == request.user

        # If the object shape is unknown, be conservative.
        return False


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    CRUD for job application owned by the authenticated user.
    - Queryset is user-scoped (zero data leakage).
    - Prefetch contacts/tasks to avoid N+1 queries
      when serializing nested read-only data.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Prefetch related to keep response fast when including nested contacts/tasks.
        return Application.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "contacts",
                queryset=Contact.objects.only("id", "name", "email", "role", "phone"),
            ),
            Prefetch(
                "tasks",
                queryset=Task.objects.only(
                    "id", "title", "due_date", "done", "created_at"
                ),
            ),
        )

    def perform_create(self, serializer):
        # Server-side assignment prevents impersonation via playload.
        serializer.save(user=self.request.user)

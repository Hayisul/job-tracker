from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Prefetch
from .models import Application, Contact, Task
from .serializers import ApplicationSerializer, ContactSerializer, TaskSerializer


class IsOwner(permissions.BasePermission):
    """
    Custom permission: only allow the owner of the object to access it.
    Works for:
      - Application (has a `user` field)
      - Contact/Task (linked to Application, which has a `user`)
    """

    def has_object_permission(self, request, view, obj):
        # If the object has a direct user field (Application).
        owner = getattr(obj, "user", None)
        if owner is not None:
            return owner == request.user

        # If the object has an application with a user (Contact/Task).
        application = getattr(obj, "application", None)
        if application is not None:
            return application.user == request.user

        # If neither case applies, deny access.
        return False


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD (Create, Read, Update, Delete) for Applications.
    - Users only see their own applications.
    - Prefetch contacts and tasks for better performance.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only applications that belong to the logged-in user.
        # Prefetch contacts/tasks so nested data loads in fewer queries.
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
        # Always set the user from the request (prevents impersonation).
        serializer.save(user=self.request.user)


class ContactViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Contacts.
    - Users only see contacts tied to their own applications.
    - When creating, the application is taken from the URL, not the request body.
    """

    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only contacts where the related application belongs to the user.
        return Contact.objects.filter(
            application__user=self.request.user
        ).select_related(
            "application"
        )  # Avoids extra queries when accessing application

    def perform_create(self, serializer):
        """
        Set the application from the URL (nested routes).
        Example: /applications/{apllication_pk}/contacts/
        """

        application_pk = self.kwargs.get("application_pk")
        if not application_pk:
            raise ValidationError(
                "Missing application context. Use a nested route with `application_pk`."
            )

        try:
            # Make sure the applcation exists and belongs to the current user.
            application = Application.objects.get(
                pk=application_pk, user=self.request.user
            )
        except Application.DoesNotExist:
            raise PermissionDenied(
                "You do not have permission to add a contact to this application."
            )

        # Save the contact linked to this application.
        serializer.save(application=application)


class TaskViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Tasks.
    - Users only see tasks tied their applications.
    - When creating, the application is taken from the URL.
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only tasks where the related application belongs to the user.
        return Task.objects.filter(application__user=self.request.user).select_related(
            "application"
        )

    def perform_create(self, serializer):
        # Get the application from the URL.
        application_pk = self.kwargs.get("application_pk")
        if not application_pk:
            raise ValidationError(
                "Missing application context. Use a nested route with `application_pk`."
            )

        try:
            application = Application.objects.get(
                pk=application_pk, user=self.request.user
            )
        except Application.DoesNotExist:
            raise PermissionDenied(
                "You do not have permission to add a task to this application."
            )

        serializer.save(application=application)

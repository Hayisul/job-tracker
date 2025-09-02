from rest_framework import serializers
from .models import Application, Contact, Task


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Application-related contacts (recruiters/HR, etc.).
    -`id` and `application` are read-only to prevent clients from mass-assigning them.
    The view should set `application` (e.g., from URL kwargs) in `perform_create`.
    """

    class Meta:
        model = Contact

        # Exposes: id, application, name, email, role, phone, notes
        fields = "__all__"

        # Protect server-owned fields; avoid alllowing the re-link contacts.
        read_only_fields = ("id", "application")


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks tied to an Application.
    - `created_at`is server-generated.
    - `application`is read-only; set in the view, not from client input.
    """

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "application", "created_at")


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Top-leel job application.
    - Includes nested, READ-ONLY lists of `contacts`and `tasks`
      to keep writes simple (no writable-nested complexity).
      Create/update them via their own endpoints.
    - `user` is read-only so clients can't impersonate owners;
      set from `request.user` in the view.
    """

    contacts = ContactSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"

        # Server-controlled fields; `user` assigned in the view;
        # timestamps managed by the model.
        read_only_fields = ("id", "user", "created_at", "updated_at")

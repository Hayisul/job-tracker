from rest_framework import serializers
from .models import Application, Contact, Task


class ContactSerializer(serializers.ModelSerializer):
    """
    Turns Contact objects into JSON and back.
    Used for contacts related to an application (like recruiters).
    """

    class Meta:
        model = Contact
        fields = "__all__"  # Include every field from the model

        # These fields cannot be set by the user.
        # - id: always auto-generated
        # - application: must be set by the view, not the client
        read_only_fields = ("id", "application")


class TaskSerializer(serializers.ModelSerializer):
    """
    Turns Task objects into JSON and back.
    Used for tasks linked to an application.
    """

    class Meta:
        model = Task
        fields = "__all__"

        # Fields the client cannot change:
        # - id: auto-generated
        # - application: set by the view
        # - created_at: set automatically when saved
        read_only_fields = ("id", "application", "created_at")


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Turns Application objects into JSON and back.
    Includes a read-only list of contacts and tasks.
    """

    # Show related contacts and tasks, but don’t allow editing them here.
    # (They each have their own endpoints for create/update.)
    contacts = ContactSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"

        # Fields that are not editable by the client:
        # - id: auto-generated
        # - user: set by the view (request.user)
        # - created_at / updated_at: managed automatically
        read_only_fields = ("id", "user", "created_at", "updated_at")

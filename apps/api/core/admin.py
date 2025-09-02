from django.contrib import admin
from .models import Application, Contact, Task


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Application model.
    Controls how job applications are displayed, filtered and searched
    in the Django admin panel.
    """

    # Columns to display in the list view (makes overview more informative).
    list_display = ("title", "company", "status", "user", "created_at")

    # Siderbar filters (helpful for quickly narrowing down large datasets).
    list_filter = ("status", "company", "created_at")

    # Searchable fields (full-text serach box at top of admin list page).
    search_fields = ("status", "company", "stage", "source", "location")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.
    Manages recruiter/HR contacts associated with applications.
    """

    list_display = ("name", "role", "email", "application")
    search_fields = ("name", "email", "role")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.
    Manages to-do tasks linked to job applications.
    """

    list_display = ("title", "application", "due_date", "done", "created_at")
    list_filter = ("done",)
    search_fields = ("title",)

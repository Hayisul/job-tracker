from django.contrib import admin
from .models import Application, Contact, Task


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Tells Django how to show the Application model in the admin site.
    """

    # Which fields to show in the list of applications.
    # (Makes it easier to see important info at a glance.)
    list_display = ("title", "company", "status", "user", "created_at")

    # Filters shown on the right side in the admin.
    # (Lets you quickly narrow down applications.)
    list_filter = ("status", "company", "created_at")

    # Fields that can be searched with the search box at the top.
    search_fields = ("status", "company", "stage", "source", "location")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Tells Django how to show the Contact model in the admin site.
    """

    # Show these fields in the list of contacts.
    list_display = ("name", "role", "email", "application")

    # Allow searching by these fields.
    search_fields = ("name", "email", "role")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Tells Django how to show the Task model in the admin site.
    """

    # Show these fields in the list of tasks.
    list_display = ("title", "application", "due_date", "done", "created_at")

    # Add a filter for "done" so you can see finished vs unfinished tasks.
    list_filter = ("done",)

    # Allow searching by task title.
    search_fields = ("title",)

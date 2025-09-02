from django.conf import settings
from django.db import models


class Application(models.Model):
    """
    Represents a job application made by a user.
    Stores metadata about the job, its status, source, salary, and tracking details.
    """

    class Status(models.TextChoices):
        """
        Enumerated job application statuses.
        Using TextChoices ensures database consistency and human-readable labels.
        """

        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    # User who owns the application.
    # Linked to the Django AUTH_USER_MODEL for flexibility.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Job-related metadata.
    title = models.CharField(max_length=200)  # e.g., Software Engineer
    company = models.CharField(max_length=200)  # Company name
    location = models.CharField(max_length=200, blank=True)  # Optional job location
    stage = models.CharField(max_length=200, blank=True)  # Custom stage

    # Predefined status (with default = applied).
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED,
    )

    # Where the job was found: LinkedIn, Referral, Job Board, etc.
    source = models.CharField(max_length=120, blank=True)

    # Optional salary expectations.
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)

    # Priority level for tracking applications (0 = low, 5 = high).
    priority = models.IntegerField(default=0)

    # Audit fields.
    created_at = models.DateField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save

    class Meta:
        """
        Meta configuration for Application model.
        - Default ordering by newest applications.
        - Indexes for common queries.
        """

        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["company"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        """Readable string representation: 'Job Title @ Company'."""
        return f"{self.title} @ {self.company}"


class Contact(models.Model):
    """
    Represents a contact person related to an application
    (e.g., recruiter, HR manager, referral).
    """

    # Link back to Application (one_to_many relationship).
    application = models.ForeignKey(
        Application,
        related_name="contacts",  # Allows reveerse lookup: application.contacts.all()
        on_delete=models.CASCADE,
    )

    # Contact details.
    name = models.CharField(max_length=120)  # Required contact name
    email = models.EmailField(blank=True)  # Optional email
    role = models.CharField(max_length=120, blank=True)  # Job role (e.g., "Recruiter")
    phone = models.CharField(max_length=50, blank=True)  # Optional phone number
    notes = models.TextField(blank=True)  # Free-form notes

    def __str__(self) -> str:
        """Readable string: 'Name (Role)."""
        return f"{self.name} ({self.role})"


class Task(models.Model):
    """
    Represents a task related to a job application
    (e.g., 'Send follow-up email', 'Prepare for interview').
    """

    # Link back to Application (one-to-many relationship).
    application = models.ForeignKey(
        Application,
        related_name="tasks",  # Allows reverse lookup: application.tasks.all()
        on_delete=models.CASCADE,
    )

    # Task details.
    title = models.CharField(max_length=200)  # Short task description
    due_date = models.DateField(null=True, blank=True)  # Optional due date
    done = models.BooleanField(default=False)  # Task completion status

    # Audit field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set on creation

    class Meta:
        """
        Task ordering rules:
        - Incomplete tasks first.
        - Oredered by due date (soonest first).
        - If same due date, ordered by creation time (latest first)
        """

        ordering = ["done", "due_date", "-created_at"]

    def __str__(self) -> str:
        """Readable string: task title"""
        return self.title

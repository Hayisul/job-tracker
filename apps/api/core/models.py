from django.conf import settings
from django.db import models


class Application(models.Model):
    """
    A job application created by a user.
    Stores information like the job title, company, status, salary, etc.
    """

    class Status(models.TextChoices):
        """
        Choices for the status of an application.
        Stored in the database as text (e.g., "applied"),
        but displayed nicely in the admin or forms (e.g., "Applied").
        """

        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    # Link each application to the user who owns it.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Job details.
    title = models.CharField(max_length=200)  # Job title (e.g., "Software Engineer")
    company = models.CharField(max_length=200)  # Company name
    location = models.CharField(max_length=200, blank=True)  # Job location (optional)
    stage = models.CharField(max_length=200, blank=True)  # Custom stage name

    # Status of the application, defaults to "applied".
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED,
    )

    # Where the job was found (LinkedIn, referral, etc.).
    source = models.CharField(max_length=120, blank=True)

    # Salary range (optional).
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)

    # Priority level for this application (0 = low, 5 = high).
    priority = models.IntegerField(default=0)

    # Automatically managed timestamps.
    created_at = models.DateField(auto_now_add=True)  # Set when created
    updated_at = models.DateTimeField(auto_now=True)  # Updated every save

    class Meta:
        """
        Extra settings for the model:
        - Show newest applications first.
        - Add indexes to make common queries faster.
        """

        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["company"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        """How this object shows up as text (useful in the admin)."""
        return f"{self.title} @ {self.company}"


class Contact(models.Model):
    """
    A contact person related to a job application
    (e.g., recruiter, HR manager, referral).
    """

    # Link to the application this contact belongs to.
    application = models.ForeignKey(
        Application,
        related_name="contacts",  # Lets us use: application.contacts.all()
        on_delete=models.CASCADE,
    )

    # Contact details.
    name = models.CharField(max_length=120)  # Contact's name
    email = models.EmailField(blank=True)  # Contact's email (optional)
    role = models.CharField(max_length=120, blank=True)  # Contact's role/job title
    phone = models.CharField(max_length=50, blank=True)  # Phone number (optional)
    notes = models.TextField(blank=True)  # Extra notes

    def __str__(self) -> str:
        """Text display for this contact (Name and Role)."""
        return f"{self.name} ({self.role})"


class Task(models.Model):
    """
    A task connected to a job application
    (e.g., "Send follow-up email", "Prepare for interview").
    """

    # Link to the application this task belongs to.
    application = models.ForeignKey(
        Application,
        related_name="tasks",  # Lets us use: application.tasks.all()
        on_delete=models.CASCADE,
    )

    # Task details.
    title = models.CharField(max_length=200)  # Task title
    due_date = models.DateField(null=True, blank=True)  # Optional deadline
    done = models.BooleanField(default=False)  # Is the task finished?

    # Automatically set when the task is created.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        How tasks are sorted:
        - Incomplete first
        - Then by due date (earliest first)
        - If same due date, newest created first
        """

        ordering = ["done", "due_date", "-created_at"]

    def __str__(self) -> str:
        """Text display for this task (just the title)."""
        return self.title

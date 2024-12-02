from django.db import models
 # Assuming User model is used for assigning leads

from userprofile.models import UserProfile


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('lost', 'Lost'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)  # New field for company
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Interaction(models.Model):
    CALL = 'Call'
    EMAIL = 'Email'
    MEETING = 'Meeting'

    INTERACTION_TYPE_CHOICES = [
        (CALL, 'Call'),
        (EMAIL, 'Email'),
        (MEETING, 'Meeting'),
    ]

    lead = models.ForeignKey(Lead, related_name='interactions', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=100, choices=INTERACTION_TYPE_CHOICES)  # Updated field
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.interaction_type} on {self.date}"

class Reply(models.Model):
    interaction = models.ForeignKey(Interaction, related_name='replies', on_delete=models.CASCADE)
    reply_text = models.TextField()
    replied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.interaction}"

class Task(models.Model):
    lead = models.ForeignKey('Lead', related_name='tasks', on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} for {self.lead.first_name} {self.lead.last_name}"
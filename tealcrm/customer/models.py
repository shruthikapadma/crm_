from django.utils import timezone

from django.db import models



# Create your models here.
class CustomerUserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Customer_details(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class task(models.Model):
    customer = models.ForeignKey('Customer_details', related_name='tasks', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    customer = models.ForeignKey(CustomerUserProfile, on_delete=models.CASCADE, related_name="support_tickets")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CustomerInteraction(models.Model):
    customer = models.ForeignKey('Customer_details', on_delete=models.CASCADE, related_name='interactions')
    date = models.DateTimeField(default=timezone.now)  # Correct way to assign the default datetime
    notes = models.TextField()
    interaction_type = models.CharField(
        max_length=50,
        choices=[
            ('Call', 'Call'),
            ('Email', 'Email'),
            ('Meeting', 'Meeting'),
            ('Other', 'Other')
        ]
    )

    def __str__(self):
        return f"{self.customer.name} - {self.interaction_type} on {self.date.strftime('%Y-%m-%d')}"
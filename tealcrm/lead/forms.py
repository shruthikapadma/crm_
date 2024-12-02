from django import forms
from .models import Lead, Interaction, Task, Reply


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'phone', 'company',  'status', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'company': 'Company Name',
            'status': 'Lead Status',
            'assigned_to': 'Assigned To',
        }


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['notes', 'interaction_type','date']  # Exclude 'date' field
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interaction_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'notes': 'Notes',
            'interaction_type': 'Interaction Type',
            'date': 'Date',
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed', 'assigned_to']  # Ensure 'assigned_to' is included if needed
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Task Title',
            'description': 'Task Description',
            'due_date': 'Due Date',
            'completed': 'Mark as Complete',
            'assigned_to': 'Assigned To',  # Include if your model has this field
        }
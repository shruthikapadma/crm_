from sqlite3 import IntegrityError

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lead, Interaction, Task
from .forms import LeadForm, InteractionForm, TaskForm , ReplyForm # Assuming forms are created for each model
from userprofile.models import UserProfile


def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'dashboard.html', {'leads': leads})


def lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    interactions = lead.interactions.all()
    tasks = lead.tasks.filter(completed=False)  # show only pending tasks
    return render(request, 'lead_detail.html', {'lead': lead, 'interactions': interactions, 'tasks': tasks})

 # Ensure only logged-in users can access this view
def create_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            assigned_user_id = request.POST.get('assigned_to')

            # Ensure assigned_to is a valid UserProfile instance
            if assigned_user_id:
                assigned_user = get_object_or_404(UserProfile, id=assigned_user_id)
                lead.assigned_to = assigned_user

            lead.save()
            messages.success(request, 'Lead created successfully.')
            return redirect('dashboard')  # Adjust to the correct URL name for your dashboard
    else:
        form = LeadForm()

    # Pass UserProfile instances to the template for the dropdown
    users = UserProfile.objects.all()
    return render(request, 'create_lead.html', {'form': form, 'users': users})

def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated successfully.')
            return redirect('dashboard')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'edit_lead.html', {'form': form, 'lead': lead})


def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    messages.success(request, 'Lead deleted successfully.')
    return redirect('dashboard')


def add_interaction(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.lead = lead
            interaction.save()
            messages.success(request, 'Interaction added successfully.')
            return redirect('lead_detail', lead_id=lead.id)
    else:
        form = InteractionForm()
    return render(request, 'add_interaction.html', {'form': form, 'lead': lead})

#
# def add_task(request, lead_id):
#     lead = get_object_or_404(Lead, id=lead_id)
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.lead = lead
#             task.save()
#             messages.success(request, 'Task added successfully.')
#             return redirect('lead_detail', lead_id=lead.id)
#     else:
#         form = TaskForm()
#     return render(request, 'add_task.html', {'form': form, 'lead': lead})


def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    messages.success(request, 'Task marked as complete.')
    return redirect('lead_detail', lead_id=task.lead.id)

def interaction_list(request):
    interactions = Interaction.objects.all()
    return render(request, 'interaction_list.html', {'interactions': interactions})


def create_interaction(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)  # Ensure lead exists
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.lead = lead  # Associate the interaction with the lead
            interaction.save()  # Save the interaction
            messages.success(request, 'Interaction created successfully.')
            return redirect('lead_detail', lead_id=lead.id)
        else:
            messages.error(request, 'Please correct the errors below.')  # Error message if form is invalid
    else:
        form = InteractionForm()
    return render(request, 'create_interaction.html', {'form': form, 'lead': lead})

def edit_interaction(request, lead_id,interaction_id):
    lead = get_object_or_404(Lead, id=lead_id)
    interaction = get_object_or_404(Interaction, id=interaction_id)
    if request.method == 'POST':
        form = InteractionForm(request.POST, instance=interaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interaction updated successfully.')
            return redirect('lead_detail', lead_id=interaction.lead.id)
    else:
        form = InteractionForm(instance=interaction)
    return render(request, 'edit_interaction.html', {'lead':lead,'form': form, 'interaction': interaction})

def delete_interaction(request, lead_id,interaction_id):
    lead = get_object_or_404(Lead, id=lead_id)
    interaction = get_object_or_404(Interaction, id=interaction_id,lead=lead)
    lead_id = interaction.lead.id  # Store lead ID for redirection
    interaction.delete()
    messages.success(request, 'Interaction deleted successfully.')
    return redirect('lead_detail', lead_id=lead_id)


def task_list(request,lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    tasks = Task.objects.all()  # Adjust this to filter tasks as needed
    return render(request, 'task_list.html', {'tasks': tasks})





def create_task(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.lead = lead  # Assign the lead to the task before saving
            try:
                task.save()
                messages.success(request, 'Task created successfully.')
                return redirect('lead_detail', lead_id=lead.id)
            except IntegrityError as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('lead_detail', lead_id=lead.id)
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form, 'lead': lead})


def lead_edit_task(request, lead_id, task_id):
    # Fetch the lead and the task associated with it
    lead = get_object_or_404(Lead, id=lead_id)  # Ensure the lead exists
    task = get_object_or_404(Task, id=task_id, lead=lead)  # Ensure the task belongs to the lead

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('lead_detail', lead_id=lead.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'lead_edit_task.html', {'form': form, 'task': task, 'lead': lead})



def lead_delete_task(request, lead_id, task_id):
    task = get_object_or_404(Task, id=task_id, lead__id=lead_id)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('lead_detail', lead_id=lead_id)
from django.shortcuts import render, get_object_or_404
from .models import Lead


def lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    interactions = lead.interactions.all()
    tasks = lead.tasks.all()# Assuming you want only pending tasks
    return render(request, 'lead_detail.html', {
        'lead': lead,
        'interactions': interactions,
        'tasks': tasks,
    })

def interaction_detail(request, interaction_id):
    interaction = get_object_or_404(Interaction, id=interaction_id)
    replies = interaction.replies.all()

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.interaction = interaction  # Associate the reply with the interaction
            reply.save()
            messages.success(request, 'Reply added successfully.')
            return redirect('interaction_detail', interaction_id=interaction.id)
    else:
        form = ReplyForm()

    return render(request, 'interaction_detail.html', {
        'interaction': interaction,
        'replies': replies,
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(username=username,password=password)

            if user:
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                return HttpResponse("invalid username or pass")
        except UserProfile.DoesNotExist:
            return HttpResponse("invalid username or pass")

    return render(request, 'login.html')

def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            # Create applicant and hash the password
            newuser = UserProfile(username=username, email=email, password=password)
            newuser.save()
            messages.success(request, "Applicant account created successfully. You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")

    return render(request, 'signup.html')
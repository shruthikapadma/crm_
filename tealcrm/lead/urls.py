from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),  # Lists all leads
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('create/', views.create_lead, name='create_lead'),  # Form for creating a new lead
    path('edit/<int:lead_id>/', views.edit_lead, name='edit_lead'),  # Edit an existing lead
    path('delete/<int:lead_id>/', views.delete_lead, name='delete_lead'),  # Delete a lead
    path('lead_detail/<int:lead_id>/', views.lead_detail, name='lead_detail'),  # Details for a specific lead

    # Interactions for a specific lead
    path('<int:lead_id>/interactions/', include([
        path('', views.interaction_list, name='interaction_list'),  # List interactions for a lead
        path('create/', views.create_interaction, name='create_interaction'),  # Create a new interaction
        path('interaction/<int:interaction_id>/reply/', views.interaction_detail, name='interaction_detail'),
        path('lead/<int:lead_id>/interactions/<int:interaction_id>/edit/', views.edit_interaction, name='edit_interaction'),
        path('interaction/<int:interaction_id>/delete/', views.delete_interaction, name='delete_interaction'),

    ])),

    # Tasks for a specific lead
    path('<int:lead_id>/tasks/', include([
        path('', views.task_list, name='task_list'),
        path('create_task/', views.create_task, name='create_task'),
        path('task/edit/<int:task_id>/', views.lead_edit_task, name='lead_edit_task'),
        path('tasks/task/<int:task_id>/delete/', views.lead_delete_task, name='lead_delete_task'),
    ]))

]

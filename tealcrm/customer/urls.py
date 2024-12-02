# urls.py (customer app)
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.customer_signup, name='customer_signup'),
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    path('customers/<int:customer_id>/tasks/', views.task_list, name='task_list'),
    path('customers/<int:customer_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('customers/<int:customer_id>/add-task/', views.add_task, name='add_task'),
    path('customers/<int:customer_id>/tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('customers/<int:customer_id>/tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    path('tickets/', views.ticket_list, name='ticket_list'),  # View all tickets
    path('tickets/create/', views.create_ticket, name='create_ticket'),  # Create a new ticket
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),

    path('select-customer/', views.select_customer_for_interaction, name='select_customer_for_interaction'),
    path('view-interaction/<int:customer_id>/', views.view_customer_interaction, name='view_customer_interaction'),
    # path('customer/<int:customer_id>/interactions/', views.customer_interaction_list, name='customer_interaction_list'),
    path('customer/<int:customer_id>/interactions/add/', views.create_customer_interaction,
         name='create_customer_interaction'),
    path('customer/<int:customer_id>/interactions/<int:interaction_id>/edit/select_customer_for_interaction.html', views.customer_edit_interaction,
         name='customer_edit_interaction'),
    path('customer/<int:customer_id>/interactions/<int:interaction_id>/delete/', views.customer_delete_interaction,
         name='customer_delete_interaction'),


]

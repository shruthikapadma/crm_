from django.contrib import admin

# Register your models here.
from .models import Lead,Interaction,Task,Reply
admin.site.register(Lead)
admin.site.register(Interaction)
admin.site.register(Task)
admin.site.register(Reply)

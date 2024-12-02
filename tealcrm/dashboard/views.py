from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from lead.models import Lead


# Create your views here.


def dashboard(request):
    # Retrieve the first lead or some specific logic to determine which lead to display
    lead = Lead.objects.first()  # Replace this with your logic to select a lead

    return render(request, 'dashboard.html', {'lead': lead, 'leads': Lead.objects.all()})

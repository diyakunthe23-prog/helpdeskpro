from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Complaint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

# ================= DASHBOARD =================
from django.core.paginator import Paginator

@login_required
def dashboard(request):

    complaints_list = Complaint.objects.all().order_by('-id')

    # SEARCH
    search = request.GET.get('search')
    if search:
        complaints_list = complaints_list.filter(title__icontains=search)

    # ✅ PAGINATION
    paginator = Paginator(complaints_list, 5)   # 5 per page
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)

    # COUNTS
    pending = Complaint.objects.filter(status="Pending").count()
    in_progress = Complaint.objects.filter(status="In Progress").count()
    resolved = Complaint.objects.filter(status="Resolved").count()

    return render(request, 'dashboard.html', {
        'complaints': complaints,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved
    })

# ================= AUTH =================
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password ❌")
            return redirect("login")

    return render(request, "login.html")


def register(request):

    if request.method == "POST":
        User.objects.create_user(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password")
        )
        return redirect("login")

    return render(request,"register.html")


def user_logout(request):
    logout(request)
    return redirect("login")

# ================= COMPLAINT =================
@login_required
def submit_complaint(request):

    if request.method == "POST":
        Complaint.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            created_by=request.user
        )
        return redirect("dashboard")

    return render(request, 'submit.html')


@login_required
def delete_complaint(request, id):
    Complaint.objects.get(id=id).delete()
    return redirect("dashboard")


@login_required
def update_status(request, id):

    complaint = Complaint.objects.get(id=id)

    if complaint.status == "Pending":
        complaint.status = "In Progress"
    elif complaint.status == "In Progress":
        complaint.status = "Resolved"

    complaint.save()
    return redirect("dashboard")

# ================= TRACK =================
@login_required
def track_complaint(request):

    complaint = None

    if request.method == "POST":
        try:
            complaint = Complaint.objects.get(id=request.POST.get("complaint_id"))
        except:
            pass

    return render(request, "track.html", {"complaint": complaint})

# ================= FILTER PAGES =================

def pending_list(request):
    complaints = Complaint.objects.filter(status="Pending")
    return render(request, "pending.html", {"complaints": complaints})

def progress_list(request):
    complaints = Complaint.objects.filter(status="In Progress")
    return render(request, "progress.html", {"complaints": complaints})

def resolved_list(request):
    complaints = Complaint.objects.filter(status="Resolved")
    return render(request, "resolved.html", {"complaints": complaints})

# ================= PDF =================
@login_required
def download_report(request, id):

    complaint = Complaint.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="complaint_{id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    p.drawString(200, 800, "HelpDeskPro Report")
    p.drawString(100, 750, f"ID: {complaint.id}")
    p.drawString(100, 720, f"Title: {complaint.title}")
    p.drawString(100, 690, f"Status: {complaint.status}")
    p.drawString(100, 660, f"User: {complaint.created_by}")
    p.drawString(100, 630, f"Date: {datetime.now()}")

    p.save()

    return response


# FILTERS
@login_required
def pending_list(request):
    complaints = Complaint.objects.filter(status="Pending", created_by=request.user)
    return render(request, "pending.html", {"complaints": complaints})

@login_required
def progress_list(request):
    complaints = Complaint.objects.filter(
        status__icontains="progress"
    )
    return render(request, "progress.html", {"complaints": complaints})


from django.db.models import Q

@login_required
def resolved_list(request):

    complaints = Complaint.objects.filter(
        status__iexact="Resolved"
    )

    return render(request, "resolved.html", {"complaints": complaints})

    
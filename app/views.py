from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Report, ReportSiteUser, SubmittedFiles
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, When

def login_page(request):
    return render(request, 'app/login_page.html')


def home(request):
    return render(request, 'app/home.html')


def admin_login():
    redirect_url = "/admin/login/?next=/admin/"
    return redirect(redirect_url)


def report_form(request):
    return render(request, 'app/report_form.html')


def report_submitted(request):
    return render(request, 'app/report_submitted.html')


def set_user(request):
    user = request.user
    if user.is_anonymous:
        try:
            anonymous_user = ReportSiteUser.objects.get(
                email="anonymous@email.com",
                username="Anonymous",
                full_name="Anonymous")
        except ObjectDoesNotExist:  # Anonymous user does not exist
            anonymous_user = ReportSiteUser(
                email="anonymous@email.com",
                username="Anonymous",
                full_name="Anonymous")
        user = anonymous_user
    return user


def submit(request):
    user = set_user(request)
    user.save()

    location = request.POST.get("location")
    if location == "Other":
        location = request.POST.get("custom_location", "").strip()
    if user.email == "anonymous@email.com":
        report_instance = Report(
            user=user,
            reportTime=timezone.now(),
            location=location,
            common_issue=request.POST["common_issue"],
            description=request.POST["description"],
            e_status=request.POST["e_status"]
        )
        report_instance.save()
    else:
        report_instance = Report(
            user=user,
            reportTime=timezone.now(),
            location=location,
            common_issue=request.POST["common_issue"],
            description=request.POST["description"],
            e_status=request.POST["e_status"],
            receive_emails=request.POST["receive_emails"]
        )
        report_instance.save()

    files = request.FILES.getlist("files")
    for file in files:
        save_file = SubmittedFiles(report=report_instance, file=file)
        save_file.save()

    return HttpResponseRedirect(reverse("Report Submitted"))


def dashboard(request):
    if hasattr(request.user, 'is_site_admin') and request.user.is_site_admin:
        reports = Report.objects.all().order_by('reportTime')
    else:
        reports = Report.objects.filter(user=request.user).order_by('reportTime')

    return render(request, 'app/dashboard.html', {'reports': reports})


def mark_addressed(request, report_id):  # Code breaks if request is taken out as a parameter
    report_instance = get_object_or_404(Report, pk=report_id)
    report_instance.update_status("3")
    return HttpResponseRedirect(reverse("Dashboard"))


def mark_in_progress(request, report_id):  # Code breaks if request is taken out as a parameter
    report_instance = get_object_or_404(Report, pk=report_id)
    report_instance.update_status("2")
    return JsonResponse({'status': 'success'})


def delete(request, report_id):  # Code breaks if request is taken out as a parameter
    report_instance = get_object_or_404(Report, pk=report_id)
    submitted_files = report_instance.files.all()
    for submitted_file in submitted_files:
        submitted_file.delete()
    report_instance.delete()
    return HttpResponseRedirect(reverse("Dashboard"))


def submit_admin_comment(request, report_id):
    report_instance = get_object_or_404(Report, pk=report_id)
    admin_comment = request.POST["admin_comment"]
    report_instance.add_admin_comment(admin_comment)
    return HttpResponseRedirect(reverse("Dashboard"))


def sort(request):
    order = request.POST.get("Order")
    if hasattr(request.user, 'is_site_admin') and request.user.is_site_admin:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(user=request.user)

    if order == "NewestFirst":
        reports = reports.order_by('-reportTime')
    elif order == "OldestFirst":
        reports = reports.order_by('reportTime')
    elif order == "ByStatus":
        status_order = Case(
            When(report_status='1', then=1),  # Not Addressed
            When(report_status='2', then=2),  # In Progress
            When(report_status='3', then=3)   # Addressed
        )
        reports = reports.annotate(status_order=status_order).order_by('status_order')

    return render(request, 'app/dashboard.html', {'reports': reports, 'order': order})
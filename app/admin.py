from django.contrib import admin
from app.models import ReportSiteUser, Report, SubmittedFiles

# Register your models here.
admin.site.register(ReportSiteUser)
admin.site.register(Report)
admin.site.register(SubmittedFiles)

from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
   path('', views.login_page, name="Login page"),
   path('home/', views.home, name="Home"),
   path('logout/', LogoutView.as_view(next_page='Login page'), name="Logout"),
   path('admin-login/', views.admin_login, name="Admin Login"),
   path('report-form/', views.report_form, name="Report Form"),
   path('dashboard/', views.dashboard, name="Dashboard"),
   path('submit/', views.submit, name="Submit"),
   path('report-submitted/', views.report_submitted, name="Report Submitted"),
   path('mark-addressed/<int:report_id>/', views.mark_addressed, name="Mark Addressed"),
   path('delete/<int:report_id>/', views.delete, name="Delete"),
   path('mark-in-progress/<int:report_id>/', views.mark_in_progress, name="Mark in Progress"),
   path('submit-admin-comment/<int:report_id>/', views.submit_admin_comment, name="Submit Admin Comment"),
   path('sort/', views.sort, name="Sort")
]

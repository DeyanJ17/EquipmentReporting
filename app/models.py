from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Adapted from https://www.pyphilly.org/know-thy-user-custom-user-models-django-allauth/


class ReportSiteUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must include email.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_site_admin = True
        user.save(using=self.db)

        return user

    
class ReportSiteUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email Address',
        unique=True,
        db_index=True
    )
    username = models.CharField(
        max_length=200,
        blank=True
    )

    full_name = models.CharField(
        max_length=200,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_site_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = ReportSiteUserManager()

    def get_full_name(self):
        return self.full_name
    
    def __str__(self):
        return f"{self.email} ({self.full_name})"


def report_file_path(instance, filename):
    if instance.report.user.email == "anonymous@email.com":
        return f'Anonymous_user_report/{filename}'
    else:
        return f'Common_user_report/Report {instance.report.id}/{filename}'


class Report(models.Model):
    user = models.ForeignKey(ReportSiteUser, on_delete=models.CASCADE)
    reportTime = models.DateTimeField()

    class Buildings(models.TextChoices):
        AQC = "1", "Aquatic and Fitness Center"
        AST = "2", "Astronomy Building"
        BRN = "3", "Bryan Hall"
        BRO = "4", "Brown Library"
        CAB = "5", "New Cabell Hall"
        COC = "6", "Cocke Hall"
        CHM = "7", "Chemistry Building"
        CLK = "8", "Clark Hall"
        CLM = "9", "Clemons Library"
        GIL = "10", "Gilmer Hall"
        MCL = "11", "McLeod Hall"
        MEC = "12", "Mechanical Engineering Building"
        MIN = "13", "Minor Hall"
        MON = "14", "Monroe Hall"
        NAU = "15", "Nau Hall"
        NHL = "16", "Newcomb Hall"
        OLS = "17", "Olsson Hall"
        RICE = "18", "Rice Hall"
        RTN = "19", "Rotunda"
        SHA = "20", "Shannon Library"
        THN = "21", "Thornton Hall"
        Other = "22", "Other"  # If choose Other, user will enter the building name, which will replace "Other" in db
    location = models.CharField(max_length=200, choices=Buildings.choices, default=Buildings.AQC)
    
    class EmailStatus(models.TextChoices):
        ReceiveAll = "1", "Receive All"
        ReceiveResolved = "2", "Receive Some"
        ReceiveNone = "3", "Receive None"
    receive_emails = models.CharField(max_length=25, choices=EmailStatus.choices, default=EmailStatus.ReceiveNone)

    class CommonIssue(models.TextChoices):
        NotCommon = "1", "N/A"
        Filter = "2", "Water Fountain Filter"
        BathroomClogged = "3", "Clogging in Bathroom"
        BathroomSupply = "4", "Bathroom Supply"
        ClassEquipment = "5", "Classroom Equipment"
    common_issue = models.CharField(max_length=30, choices=CommonIssue.choices, default=CommonIssue.NotCommon)

    description = models.CharField(max_length=5000)

    class EquipmentStatus(models.TextChoices):
        Functioning = "1", "Functioning"
        Problematic = "2", "Problematic"
        Unusable = "3", "Unusable"
    e_status = models.CharField(max_length=15, choices=EquipmentStatus.choices, default=EquipmentStatus.Functioning)

    files = models.ManyToManyField('SubmittedFiles', related_name='reports', blank=True)

    # Only site admin should be able to change this
    class ReportStatus(models.TextChoices):
        NotAddressed = "1", "Not Addressed"
        InProgress = "2", "In Progress"
        Addressed = "3", "Addressed"
    report_status = models.CharField(max_length=15, choices=ReportStatus.choices, default=ReportStatus.NotAddressed)

    admin_comment = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.description

    def update_status(self, new_status):
        self.report_status = new_status
        d = {"1": "Not Addressed", "2": "In Progress", "3": "Addressed"}
        if(self.receive_emails == "receive all" or (self.receive_emails == "receive some" and new_status == "3")):
            send_mail(
            "Report Status Update",
            "Your report of an equiptment issue has been updated to " + d[new_status],
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
            )
        self.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def add_admin_comment(self, comment):
        self.admin_comment = comment
        self.save()


class SubmittedFiles(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    file = models.FileField(upload_to=report_file_path, blank=True, null=True)

    def __str__(self):
        return str(self.file)

@receiver(post_delete, sender=SubmittedFiles)
def submitted_files_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)

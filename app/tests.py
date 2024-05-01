
from django.test import TestCase
from unittest.mock import patch
from .models import ReportSiteUser, report_file_path, Report
from datetime import datetime, timedelta


class ReportSiteUserManagerTest(TestCase):
    def test_create_user_basic(self):
        # Info for auth
        email = "email@email.com"
        password = "password"

        # Create our user
        new_user = ReportSiteUser.objects.create_user(email, password)

        # Check basic info is correct
        self.assertIsNotNone(new_user)
        self.assertIsInstance(new_user, ReportSiteUser)
        self.assertEqual(new_user.email, email)
        self.assertIsNotNone(new_user.password)

        # Check perms
        self.assertFalse(new_user.is_site_admin)
        self.assertFalse(new_user.is_superuser)
        self.assertFalse(new_user.is_staff)
        
    

    def test_create_user_superuser(self):
        # Info for auth
        email = "admin@admin.com"
        password = "password"

        # Create our SUPER user
        new_user = ReportSiteUser.objects.create_superuser(email, password)

        # Check basic info is correct
        self.assertIsNotNone(new_user)
        self.assertIsInstance(new_user, ReportSiteUser)
        self.assertEqual(new_user.email, email)
        self.assertIsNotNone(new_user.password)

        # Check perms
        self.assertTrue(new_user.is_site_admin)
        self.assertTrue(new_user.is_superuser)
        self.assertTrue(new_user.is_staff)
        
    def test_create_user_no_email(self):
        # Info for auth
        email = ""
        password = "password"
        
        with self.assertRaises(ValueError):
            new_user = ReportSiteUser.objects.create_user(email, password)
            
    def test_create_user_no_password(self):
        # Info for auth
        email = "email@email.com"
        password = ""
        
        new_user = ReportSiteUser.objects.create_user(email, password)
        
        self.assertIsNotNone(new_user)
        self.assertIsInstance(new_user, ReportSiteUser)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))
        
    def test_create_superuser_no_email(self):
        # Info for auth
        email = ""
        password = "password"
        
        with self.assertRaises(ValueError):
            new_user = ReportSiteUser.objects.create_superuser(email, password)
            
    def test_create_superuser_no_password(self):
        # Info for auth
        email = "email@email.com"
        password = ""
        
        new_user = ReportSiteUser.objects.create_superuser(email, password)
        
        self.assertIsNotNone(new_user)
        self.assertIsInstance(new_user, ReportSiteUser)
        self.assertEqual(new_user.email, email)
        self.assertTrue(new_user.check_password(password))
        
       
        
        
            

    
    
    


class SubmittedFilesTest(TestCase):
    @patch('app.models.SubmittedFiles')
    @patch('app.models.Report')
    def test_report_file_path_anonymous(self, mock_report, mock_submitted_files):

        # Create file
        filename = "anonymous_file"

        # Mock mock_report
        email = "anonymous@email.com"
        mock_report_instance = mock_report.return_value
        mock_report_instance.user.email = email

        # Mock mock_submitted_files
        mock_submitted_files_instance = mock_submitted_files.return_value
        mock_submitted_files_instance.report = mock_report_instance

        expected = f"Anonymous_user_report/{filename}"

        self.assertEqual(expected, report_file_path(mock_submitted_files_instance, filename))

    @patch('app.models.SubmittedFiles')
    @patch('app.models.Report')
    def test_report_file_path_user(self, mock_report, mock_submitted_files):
        # Create file
        filename = "file"

        # Mock mock_report
        email = "file@email.com"
        mock_report_instance = mock_report.return_value
        mock_report_instance.user.email = email

        # Mock mock_submitted_files
        mock_submitted_files_instance = mock_submitted_files.return_value
        mock_submitted_files_instance.report = mock_report_instance

        expected = f"Common_user_report/Report {mock_report_instance.id}/{filename}"

        self.assertEqual(expected, report_file_path(mock_submitted_files_instance, filename))
        
class ReportTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = ReportSiteUser.objects.create_user("test@example.com", "password")
        # Create a report associated with the user
        self.report = Report.objects.create(description="Test report", reportTime=datetime.now()- timedelta(days=1), user=self.user)

    def test_update_status(self):
        new_status = "2"  
        self.report.update_status(new_status)
        self.assertEqual(self.report.report_status, new_status)

    def test_str_method(self):
        self.assertEqual(str(self.report), self.report.description)

    def test_default_report_status(self):
        self.assertEqual(self.report.report_status, "1")  

    def test_default_equipment_status(self):
        self.assertEqual(self.report.e_status, "1")  



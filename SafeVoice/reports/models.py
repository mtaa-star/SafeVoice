from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class ViolenceReport(models.Model):
    VIOLENCE_TYPES = [
        ('physical', 'Physical Violence'),
        ('sexual', 'Sexual Violence'),
        ('emotional', 'Emotional Abuse'),
        ('economic', 'Economic Abuse'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('handled', 'Handled'),
    ]

    # Add location choices - All 47 Kenyan Counties
    LOCATION_CHOICES = [
        ('mombasa', 'Mombasa'),
        ('kwale', 'Kwale'),
        ('kilifi', 'Kilifi'),
        ('tana_river', 'Tana River'),
        ('lamu', 'Lamu'),
        ('taita_taveta', 'Taita Taveta'),
        ('garissa', 'Garissa'),
        ('wajir', 'Wajir'),
        ('mandera', 'Mandera'),
        ('marsabit', 'Marsabit'),
        ('isiolo', 'Isiolo'),
        ('meru', 'Meru'),
        ('tharaka_nithi', 'Tharaka Nithi'),
        ('embu', 'Embu'),
        ('kitui', 'Kitui'),
        ('machakos', 'Machakos'),
        ('makueni', 'Makueni'),
        ('nyandarua', 'Nyandarua'),
        ('nyeri', 'Nyeri'),
        ('kirinyaga', 'Kirinyaga'),
        ('muranga', "Murang'a"),
        ('kiambu', 'Kiambu'),
        ('turkana', 'Turkana'),
        ('west_pokot', 'West Pokot'),
        ('samburu', 'Samburu'),
        ('trans_nzoia', 'Trans Nzoia'),
        ('uasin_gishu', 'Uasin Gishu'),
        ('elgeyo_marakwet', 'Elgeyo Marakwet'),
        ('nandi', 'Nandi'),
        ('baringo', 'Baringo'),
        ('laikipia', 'Laikipia'),
        ('nakuru', 'Nakuru'),
        ('narok', 'Narok'),
        ('kajiado', 'Kajiado'),
        ('kericho', 'Kericho'),
        ('bomet', 'Bomet'),
        ('kakamega', 'Kakamega'),
        ('vihiga', 'Vihiga'),
        ('bungoma', 'Bungoma'),
        ('busia', 'Busia'),
        ('siaya', 'Siaya'),
        ('kisumu', 'Kisumu'),
        ('homa_bay', 'Homa Bay'),
        ('migori', 'Migori'),
        ('kisii', 'Kisii'),
        ('nyamira', 'Nyamira'),
        ('nairobi', 'Nairobi'),
    ]
    
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    violence_type = models.CharField(max_length=20, choices=VIOLENCE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.violence_type} - {self.submitted_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Violence Report'
        verbose_name_plural = 'Violence Reports'

class FollowUp(models.Model):
    report = models.ForeignKey(ViolenceReport, on_delete=models.CASCADE, related_name='follow_ups')
    contact = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report Follow Up'
        verbose_name_plural = 'Report Follow Ups'

    def __str__(self):
        return f"Follow-up for report {self.report.id} by {self.contact} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AdminLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Logged In'),
        ('logout', 'Logged Out'),
        ('view_report', 'Viewed Report'),
        ('create_report', 'Created Report'),
        ('update_status', 'Updated Report Status'),
        ('edit_report', 'Edited Report'),
        ('delete_report', 'Deleted Report'),
        ('download_evidence', 'Downloaded Evidence'),
        ('export_data', 'Exported Data'),
        ('filter_reports', 'Filtered Reports'),
        ('search_reports', 'Searched Reports'),
    ]
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    report_id = models.IntegerField(null=True, blank=True)  # Related report if applicable
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Admin Activity Log'
        verbose_name_plural = 'Admin Activity Logs'
    
    def __str__(self):
        return f"{self.admin_user.username if self.admin_user else 'Unknown'} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
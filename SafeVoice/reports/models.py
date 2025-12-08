from django.db import models
from django.utils import timezone
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
    
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    violence_type = models.CharField(max_length=20, choices=VIOLENCE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=300)
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.violence_type} - {self.submitted_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Violence Report'
        verbose_name_plural = 'Violence Reports'
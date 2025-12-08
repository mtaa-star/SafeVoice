from django.contrib import admin
from .models import ViolenceReport
# Register your models here.
@admin.register(ViolenceReport)
class ViolenceReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact', 'violence_type', 'location', 'submitted_at']
    list_filter = ['violence_type', 'submitted_at']
    search_fields = ['name', 'contact', 'location', 'description']
    readonly_fields = ['submitted_at']
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Reporter Information', {
            'fields': ('name', 'contact')
        }),
        ('Incident Details', {
            'fields': ('violence_type', 'description', 'location')
        }),
        ('Evidence', {
            'fields': ('evidence_file',)
        }),
        ('System Information', {
            'fields': ('submitted_at',)
        }),
    )
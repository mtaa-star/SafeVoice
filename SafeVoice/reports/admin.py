from django.contrib import admin
from .models import ViolenceReport
from .models import ViolenceReport, AdminLog
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

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'admin_user', 'action', 'report_id', 'ip_address']
    list_filter = ['action', 'timestamp', 'admin_user']
    search_fields = ['admin_user__username', 'description', 'ip_address']
    readonly_fields = ['timestamp', 'admin_user', 'action', 'description', 'report_id', 'ip_address']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False  # Prevent manual creation
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion for audit trail integrity
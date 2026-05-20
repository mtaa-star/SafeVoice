from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import ViolenceReportForm
from .models import ViolenceReport
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ViolenceReport, AdminLog  # Add AdminLog
import json


def send_admin_email(report):
    admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', '')
    if not admin_email:
        return False

    subject = f"New GBV Report Submitted: {report.get_violence_type_display()}"
    message = (
        f"A new report has been submitted.\n\n"
        f"Name: {report.name}\n"
        f"Contact: {report.contact}\n"
        f"Type: {report.get_violence_type_display()}\n"
        f"Location: {report.get_location_display()}\n"
        f"Submitted At: {report.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Details:\n{report.description}\n"
    )

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Admin email notification failed: {e}")
        return False


def send_admin_sms(report):
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_number = getattr(settings, 'TWILIO_FROM_NUMBER', '')
    to_number = getattr(settings, 'ADMIN_NOTIFICATION_PHONE', '')
    if not all([account_sid, auth_token, from_number, to_number]):
        return False

    body = (
        f"New GBV report from {report.name}: {report.get_violence_type_display()} in "
        f"{report.get_location_display()}. Contact {report.contact}. Submitted at "
        f"{report.submitted_at.strftime('%Y-%m-%d %H:%M')}."
    )

    try:
        data = urllib.parse.urlencode({
            'From': from_number,
            'To': to_number,
            'Body': body,
        }).encode()
        auth_str = f"{account_sid}:{auth_token}"
        auth_header = base64.b64encode(auth_str.encode()).decode()
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Authorization', f'Basic {auth_header}')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')

        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status in (200, 201)
    except Exception as e:
        print(f"Admin SMS notification failed: {e}")
        return False


def notify_admin(report):
    email_sent = send_admin_email(report)
    if not email_sent:
        print('Admin notification email was not sent. Check ADMIN_NOTIFICATION_EMAIL setting.')
    return email_sent

# Create your views here.
# Add this new view
# Helper function to log admin activities
def log_admin_activity(user, action, description, report_id=None, request=None):
    """Log administrator activities for audit trail"""
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    try:    
        AdminLog.objects.create(
           admin_user=user,
           action=action,
           description=description,
           report_id=report_id,
           ip_address=ip_address
        )
        print(f"Log created: {user} - {action}") #debug print statement
    except Exception as e:
        print(f"Error occurred while logging admin activity: {e}") #debug print statement

def landing_page(request):
    """Display the landing page with GBV information"""
    return render(request, 'landing.html')

def report_violence(request):
    if request.method == 'POST':
        form = ViolenceReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            notify_admin(report)
            messages.success(request, 'Your report has been submitted successfully. Thank you for your courage.')
            return redirect('report_success')
    else:
        form = ViolenceReportForm()
    
    return render(request, 'reports/report_form.html', {'form': form})

def report_success(request):
    return render(request, 'reports/success.html')

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
    #if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            if user.is_staff:
                login(request, user)
                # Log the admin login activity
                log_admin_activity(
                    user=user,
                    action='login',
                    description=f'Admin {user.username} logged into the system successfully.',
                    request=request
                )
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You do not have permission to access the admin dashboard.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
           # login(request, user)
           # return redirect('admin_dashboard')
       # else:
         #   messages.error(request, 'Invalid credentials or insufficient permissions.')"""
    
    return render(request, 'reports/admin_login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    reports = ViolenceReport.objects.all()
    #Log dashboard access
    log_admin_activity(
        user=request.user,
        action='view_report',
        description=f'Admin {request.user.username} accessed the dashboard.',
        request=request
    )
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    # Filter by violence type if provided
    type_filter = request.GET.get('type')
    if type_filter:
        reports = reports.filter(violence_type=type_filter)
    
    context = {
        'reports': reports,
        'total_reports': ViolenceReport.objects.count(),
        'pending_count': ViolenceReport.objects.filter(status='pending').count(),
        'in_progress_count': ViolenceReport.objects.filter(status='in_progress').count(),
        'handled_count': ViolenceReport.objects.filter(status='handled').count(),
    }
    
    return render(request, 'reports/admin_dashboard.html', context)

@login_required(login_url='admin_login')
def edit_report(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    report = get_object_or_404(ViolenceReport, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'in_progress', 'handled']:
            report.status = status
            report.save()
            log_admin_activity(
                user=request.user,
                action='edit_report',
                description=f'Admin {request.user.username} updated report {report.id}.',
                request=request
            )
            messages.success(request, 'Report updated successfully.')
        return redirect('admin_dashboard')
    
    return render(request, 'reports/edit_report.html', {'report': report})

@login_required(login_url='admin_login')
def delete_report(request, pk):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    report = get_object_or_404(ViolenceReport, pk=pk)
    
    if request.method == 'POST':
        report.delete()
        log_admin_activity(
            user=request.user,
            action='delete_report',
            description=f'Admin {request.user.username} deleted report {report.id}.',
            request=request
        )
        messages.success(request, 'Report deleted successfully.')
        return redirect('admin_dashboard')
    
    return render(request, 'reports/delete_confirm.html', {'report': report})

@login_required
def admin_logout(request):
    # Log the admin logout activity before logging out
    log_admin_activity(
        user=request.user,
        action='logout',
        description=f'Admin {request.user.username} logged out of the system.',
        request=request
    )
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

@login_required(login_url='admin_login')
def admin_logs(request):
    """View to display admin activity logs"""
    if not request.user.is_staff:
        return redirect('admin_login')
    
    logs = AdminLog.objects.all()
    
    # Filter by admin user if provided
    user_filter = request.GET.get('user')
    if user_filter:
        logs = logs.filter(admin_user__username=user_filter)
    
    # Filter by action if provided
    action_filter = request.GET.get('action')
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(timestamp__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__lte=date_to)
    
    # Get list of all admin users for filter dropdown
    from django.contrib.auth.models import User
    admin_users = User.objects.filter(is_staff=True)
    
    context = {
        'logs': logs,
        'admin_users': admin_users,
        'total_logs': AdminLog.objects.count(),
    }
    
    return render(request, 'reports/admin_logs.html', context)

@csrf_exempt
def chatbot_api(request):
    """
    API endpoint for the AI chatbot
    Note: In production, you should add proper CSRF protection
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # The chatbot will be handled on the frontend using Claude API
            # This endpoint can be used for logging or additional backend processing
            
            return JsonResponse({
                'status': 'success',
                'message': 'Message received'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests allowed'
    }, status=405)
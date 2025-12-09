from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import ViolenceReportForm
from .models import ViolenceReport
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def report_violence(request):
    if request.method == 'POST':
        form = ViolenceReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
        messages.success(request, 'Report deleted successfully.')
        return redirect('admin_dashboard')
    
    return render(request, 'reports/delete_confirm.html', {'report': report})

@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

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
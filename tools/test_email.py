import os, django, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE','SafeVoice.settings')
django.setup()
from django.core.mail import send_mail
try:
    result = send_mail(
        'SafeVoice test email',
        'This is a test email from SafeVoice.',
        'no-reply@example.com',
        ['ogalsteve00@gmail.com'],
        fail_silently=False,
    )
    print('SEND_OK', result)
except Exception:
    traceback.print_exc()

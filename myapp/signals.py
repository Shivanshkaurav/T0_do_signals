from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Todo
from django.core.mail import send_mail
from datetime import timedelta
import datetime
from django.conf import settings

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    user = request.user
    today = datetime.date.today()
    date = today + timedelta(days=3)
    tasks = Todo.objects.filter(user=user)

    for i in tasks:
        email = user.email
        subject = f'Reminder, your task is due soon!'
        message = f'Dear {i.user},\n\nYour task, {i.task} is due on {i.due_date}. Please complete it as soon as possible.\n\nThankyou'
        if i.due_date == date:
            print("sending mail")
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

    
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import render

def home_view(request):
    return render(request, 'accounts/home.html')
from .models import CustomUser

from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # לינקים
            approve_link = request.build_absolute_uri(
                reverse('approve_user', args=[user.pk])
            )
            reject_link = request.build_absolute_uri(
                reverse('reject_user', args=[user.pk])
            )

            # תוכן המייל
            subject = "🛂 משתמש חדש ממתין לאישור"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ["ori1230302@gmail.com"]  # שים את שלך

            text_content = f"""
משתמש חדש נרשם:
שם משתמש: {user.username}
אימייל: {user.email}
טלפון: {user.phone_number}
"""

            html_content = render_to_string("emails/approval_email.html", {
                'username': user.username,
                'email': user.email,
                'phone': user.phone_number,
                'approve_link': approve_link,
                'reject_link': reject_link,
            })

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "ההרשמה הצליחה! המתן לאישור מנהל.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


from django.shortcuts import get_object_or_404
from django.http import HttpResponse

def approve_user_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.is_approved = True
    user.is_active = True
    user.save()
    return HttpResponse(f"המשתמש {user.username} אושר בהצלחה ✅")

from django.http import HttpResponse

def reject_user_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    username = user.username
    user.delete()
    return HttpResponse(f"המשתמש {username} נמחק ❌")

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_approved:
            messages.error(self.request, "החשבון שלך ממתין לאישור מנהל.")
            return redirect('login')
        
        return super().form_valid(form)
@login_required
def dashboard_view(request):
    user = request.user
    return render(request, 'accounts/dashboard.html', {'user': user})


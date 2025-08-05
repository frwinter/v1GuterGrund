from django.contrib.auth.decorators import login_required  # Wichtig: Dieser Import fehlt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import RegisterForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import User
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views import View  
from .decorators import rate_limit  
from django.db import IntegrityError
from django.urls import reverse  
from django.shortcuts import render   
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

User = get_user_model()

@method_decorator(never_cache, name='dispatch')
class ActivateAccount(View):
    def get(self, request, token):
        try:
            user = User.objects.get(activation_token=token)
            if (timezone.now() - user.date_joined).days < 1:  # 24h Gültigkeit
                user.is_active = True
                user.activation_token = ""
                user.save()
                messages.success(request, "Aktivierung erfolgreich!")
                return redirect('login')
        except User.DoesNotExist:
            pass
        
        messages.error(request, "Ungültiger oder abgelaufener Link")
        return redirect('home')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            form.add_error(None, "Ihr Account ist nicht aktiviert. Bitte überprüfen Sie Ihre E-Mails.")
            return self.form_invalid(form)
        return super().form_valid(form)



def activate_account(request, token):
    try:
        user = User.objects.get(activation_token=token)
        if user.is_activation_token_valid() and not user.is_active:
            user.is_active = True
            user.activation_token = ""
            user.save()
            messages.success(request, "Ihr Account wurde erfolgreich aktiviert! Sie können sich jetzt einloggen.")
            return redirect('users:login')
        else:
            messages.error(request, "Der Aktivierungslink ist ungültig oder abgelaufen.")
    except User.DoesNotExist:
        messages.error(request, "Ungültiger Aktivierungslink.")
    return redirect('/')  # Absolute URL als Fallback


def registration_complete(request):
    """Zeigt die Bestätigungsseite nach der Registrierung an"""
    return render(request, 'registration/registration_complete.html')

def send_activation_email(request, user):
    print("\n=== MAILVERSAND START ===")
    print(f"E-Mail-Adresse: {user.email}")
    print(f"Token: {user.activation_token}")
    
    try:
        subject = "Bitte aktivieren Sie Ihren Account"
        message = render_to_string('registration/activation_email.html', {
            'user': user,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
            'token': user.activation_token,
        })
        
        print("Mail-Inhalt generiert")
        print("Speicherort:", settings.EMAIL_FILE_PATH)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        print("E-Mail erfolgreich gesendet")
    except Exception as e:
        print("FEHLER beim E-Mail-Versand:", str(e))
        raise  # Wirft den Fehler für das Debugging
    
    print("=== MAILVERSAND ENDE ===\n")

@rate_limit()
def resend_activation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            
            # Erneut Aktivierungsmail senden
            send_activation_email(request, user)

            
            messages.success(request, "Aktivierungslink wurde erneut gesendet!")
            return redirect('users:registration_complete')
            
        except User.DoesNotExist:
            messages.error(request, "Kein inaktiver Account mit dieser E-Mail gefunden.")
            return redirect('users:registration_complete')
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')  # Template mit Links zu Apps

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.generate_activation_token()
            user.save()
            
            request.session['registered_email'] = user.email
            send_activation_email(request, user)
            
            return redirect('users:registration_complete')
    else:
        form = RegisterForm()
    
    # Debug-Ausgabe für Entwickler
    if request.method == 'POST' and form.errors:
        print("Formularfehler aufgetreten:")
        for field, errors in form.errors.items():
            print(f"{field}: {', '.join(errors)}")
    
    return render(request, 'registration/register.html', {
        'form': form,
        'password_help': """
            <small class="form-text text-muted">
                Passwortanforderungen:<br>
                - Mindestens 8 Zeichen<br>
                - Nicht nur Zahlen<br>
                - Nicht zu ähnlich mit Benutzername<br>
                - Kein häufig genutztes Passwort
            </small>
        """
    })
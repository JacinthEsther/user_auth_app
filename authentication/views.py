from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User


# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'hasError': False

        }
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password should be at least six characters long')
            context['hasError'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Password does not match')
            context['hasError'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please provide a valid email')
            context['hasError'] = True
        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'email is taken')
                context['hasError'] = True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'username is taken')
                context['hasError'] = True
        except Exception as identifier:
            pass

        if context['hasError']:
            return render(request, 'auth/register.html', context, status=400)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        user.is_active = False

        user.save()

        messages.add_message(request, messages.SUCCESS, 'account created successfully')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

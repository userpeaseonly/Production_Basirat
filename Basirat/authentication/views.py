from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            # Handle invalid login credentials
            return render(request, 'authentication/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'authentication/login.html')

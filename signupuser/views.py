from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from fifa.models import Profile  # Ensure the import is correctly capitalized if you updated the model name
from django.contrib.auth import authenticate, login as auth_login

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                user.save()

                # Create a profile instance for the new user
                new_profile = Profile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    emailaddress=email
                )
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signupuser/registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            

            return redirect('home')
        else:
            # Return an 'invalid login' error message
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    else:
        return render(request, 'signupuser/login.html')
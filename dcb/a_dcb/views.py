from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Complaint
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as userLogin, logout as userLogout
from django.contrib import messages
# Create your views here.

def HOME(request):
    return render(request,'index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            userLogin(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password Didn't Match ")
            return render(request,'Memberlogin.html')
    return render(request,'Memberlogin.html')

@login_required(login_url='login')
def complaint(request):
    if request.POST:
        complaint = Complaint.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            contact = request.POST['contact'],
            complaint = request.POST['complaint'],
            file = request.FILES['files'],
        )
        
        complain_context = {
            'name': complaint.name,
            'email': complaint.email,
            'contact': complaint.contact,
            'complaint': complaint.complaint,
        }
        ownerMail = []
        ownerMail.append(settings.EMAIL_HOST_USER)
        ownerMail.append(complaint.email)
        msg = EmailMessage(f'New Complaint', render_to_string(
        'mail.html', complain_context), settings.EMAIL_HOST_USER, ownerMail)
        msg.content_subtype = "html"
        msg.attach_file(f'{complaint.file}')
        msg.send()
        return redirect('thankyou')
    return render(request,  'complaint_form.html')

@login_required(login_url='login')
def thankyou(request):
    return render(request,  'thankyou.html')

@login_required(login_url='login')
def logout(request):
    userLogout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        email = request.POST['email']

        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username Already Taken')
            return render(request,  'memberregister.html')
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Registered Successfully')
    return render(request,  'memberregister.html')
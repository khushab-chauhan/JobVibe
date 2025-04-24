from django.shortcuts import render , redirect
from apps.users.models import User
from django.contrib import messages
from apps.master.utils.email_varify import email_varify
from apps.master.utils.otp_generator import otp_generator
from apps.master.utils.password_varify import password_varify
# Create your views here.


def login_page(request):
    return render(request,'dashboard/login.html')
def register_page(request):
    if request.method == "POST":
        account_type_  = request.POST['account_type']
        email_  = request.POST['email']
        password_  = request.POST['password']
        confirm_password_ = request.POST['confirm_password']

        if not email_varify(email_):
            messages.error(request,"invalid email")
            return redirect('register')
        

        if not password_varify(password_)[0]:
            messages.error(request,password_varify(password_)[1])
            return redirect('register')

        if password_ != confirm_password_:
            messages.error(request,"password not match") 
            return redirect('register')
        
        if User.objects.filter(email = email_).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
    
        InnerQuerySet = User.objects.create(
            account_type = account_type_,
            email = email_,
            password = password_
        )
        InnerQuerySet.save()
        return redirect('login')
    return render(request,'dashboard/register.html')

def dashboard_page(request):
    return render(request,'dashboard/dashboard.html')
def forgot_password_page(request):
    return render(request,'dashboard/forgot_password.html')
def otp_password_page(request):
    return render(request,'dashboard/otp_password.html')
def otp_register_page(request):
    return render(request,'dashboard/otp_register.html')

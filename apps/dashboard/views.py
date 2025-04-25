from django.shortcuts import render , redirect
from apps.users.models import User
from django.contrib import messages
from apps.master.utils.email_varify import email_varify
from apps.master.utils.otp_generator import otp_generator
from apps.master.utils.password_varify import password_varify
from django.core.mail import send_mail
from django.conf import settings
from functools import  wraps
from django.contrib.auth.decorators import login_required
# Create your views here.


def login_requirement(my_function):
    @wraps(my_function)
    def  _wrapped(request,*args,**kwargs):
        if 'user_id' not in request.session:
            messages.error(request,'You must be logged in to access this page.')
            return redirect('login')
        
        return my_function(request,*args,**kwargs)
    return _wrapped

def youcannot_access(my_function):
    @wraps(my_function)
    def  _wrapped(request,*args,**kwargs):
        if 'user_id' not in request.session:
            messages.error(request,'does not have page.')
            return redirect('login')
        
        return my_function(request,*args,**kwargs)
    return _wrapped


def login_page(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_  = request.POST['password']

        if not email_varify(email_):
            messages.error(request,"invalid email")
            return redirect('login') 
        
        if not User.objects.filter(email = email_ ).exists():
            messages.error(request,"email does not exits")
            return redirect('login') 
        else:
            user = User.objects.get(email = email_)
            if password_ == user.password:
                request.session['user_id'] = str(user.id)
                print(request.session['user_id'])
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password')
                return redirect('login')



    return render(request,'dashboard/login.html')


def register_page(request):
    if request.method == "POST":
        account_type_  = request.POST['account_type']
        email_  = request.POST['email']
        password_  = request.POST['password']
        confirm_password_ = request.POST['confirm_password']
        otp_ = request.POST['otp']



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
        
        otp_ = otp_generator()

        request.session['account_type'] = account_type_
        request.session['email'] = email_
        request.session['password'] = password_
        request.session['otp'] = otp_


        send_mail(
            subject = "Welcome to Jobbrige! 🎉",
            message= f"Hi there {email_},\n\nWelcome to Jobbrige! Your OTP for registration is: {otp_}.\n\nHappy Job Hunting!\nTeam Jobbrige",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[email_],
            fail_silently= False,
        )
        messages.success(request,"otp send your email")
        return redirect('otp_register')
    return render(request,'dashboard/register.html')



def forgot_password_page(request):
    if request.method == 'POST':
        email_ = request.POST['email']

        if not email_varify(email_):
            messages.error(request,"invalid email")
            return redirect('forgot')
        
        if not User.objects.filter(email = email_).exists():
            messages.error(request, 'Email Does not match')
            return redirect('forgot')
        else:
            user = User.objects.get(email = email_)
            otp_ = otp_generator()
            send_mail(
                subject="Reset Your Password - Jobbrige",
                message= f"Hi there {email_},\n\nWelcome to Jobbrige! Your OTP to reset password is: {otp_}.\n\nHappy Job Hunting!\nTeam Jobbrige",
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[email_],
                fail_silently=False
            )
            user.otp = otp_

            user.save()

        messages.success(request, "OTP sent to your email.")
        return render(request,'dashboard/otp_password.html',{'email':email_})


    return render(request,'dashboard/forgot_password.html')


@login_requirement
def otp_password_page(request):
    if request.method == "POST":
        email_  = request.POST['email']
        password_  = request.POST['password']
        confirm_password_ = request.POST['confirm_password']
        otp_ = request.POST['otp']

        print(email_,password_,confirm_password_,otp_)
        if not email_varify(email_):
            messages.error(request, 'Invalid email')
            return render(request, 'dashboard/otp_password.html', {'email':email_})
        
        if not User.objects.filter(email=email_).exists():
            messages.error(request, 'Email does not exist')
            return render(request, 'dashboard/otp_password.html', {'email':email_})
        else:
            user = User.objects.get(email = email_)
            if user.otp == otp_:
                if password_ !=confirm_password_:
                    messages.error(request, 'Passwords do not match')
                    return render(request, 'dashboard/otp_password.html', {'email':email_})
                
                if not password_varify(password_)[0]:
                    messages.error(request, password_varify(password_)[1])
                    return render(request, 'dashboard/otp_password.html', {'email':email_})
                
                user.password = password_
                user.save()
                messages.success(request, "Password has been changed successfully")
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'dashboard/otp_password.html', {'email':email_})
        
    return render(request,'dashboard/otp_password.html')


@login_requirement
def otp_register_page(request):
    if request.method == "POST":
        new_otp = request.POST['otp']

        otp_ = request.session.get('otp')
        email_ = request.session.get('email')
        password_ = request.session.get('password')
        account_type_ = request.session.get('account_type')

        if new_otp == otp_:
            user = User.objects.create(
                email = email_,
                account_type = account_type_,
                password = password_,
                otp = otp_
            )
            user.save()

            send_mail(
                subject="Welcome to Jobbrige! 🎉",
                message=f"Hi {user.email}, your account has been successfully created!",
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[email_],
                fail_silently=False
            )

            request.session.flush()
            messages.success(request, "OTP Verified! Account Created.")
            return redirect('login')   
        
        else:
            messages.error(request, "Invalid OTP")
            return redirect('otp_register')



    return render(request,'dashboard/otp_register.html')



@youcannot_access
@login_requirement
def dashboard_page(request):
    return render(request,'dashboard/dashboard.html')
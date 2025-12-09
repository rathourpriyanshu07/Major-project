from django.shortcuts import render
from .models import User
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def category(request):
    return render(request,'category.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                request.session['profile_picture']=user.profile_picture.url  
                return render(request,'index.html')
            else:
                msg="Incorrect password" 
                return render(request,'login.html',{'msg':msg}) 

        except:
               msg="Email Not Registerd" 
               return render(request,'login.html',{'msg':msg})      
    else:
        return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'login.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    profile_picture=request.FILES['profile_picture'],
                )
                msg="User Sign Up Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does Not Matched"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
    

def logout(request):
    try:
        del request.session['email']       
        del request.session['fname']    
        del request.session['profile_picture'] 
        msg="Logged out succesfully"
        return render(request,'login.html',{'msg':msg})    
    except:
         msg="Logged out succesfully"
         return render(request,'login.html',{'msg':msg})      


def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_picture=request.FILES['profile_picture']
        except:
            pass
        user.save()
        request.session['profile_picture']=user.profile_picture.url
        msg="profile updated successfully" 
        return render(request,'profile.html',{'user':user,'msg':msg})
    else:
        return render(request,'profile.html',{'user':user})
    
def change_password(request):
    if request.method=='POST':
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']    
                    user.save()
                    del request.session['email']       
                    del request.session['fname']    
                    del request.session['profile_picture'] 
                    msg="Password changed Succesfully"
                    return render(request, 'login.html', {'msg': msg}) 
                else:
                    msg="your new password cant be from your old password"
                    return render(request, 'change-password.html', {'msg': msg})   

            else:
                msg="New password & confirm new password does not matched" 
                return render(request,'change-password.html',{'msg':msg})
        else:
            msg="old password does not matched"
            return render(request,'change-password.html',{'msg':msg})    
    else:
        return render(request,'change-password.html')
    

def forgot_password(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            context = {}
            address = request.POST['email']
            subject = "OTP For Forgot Password"
            message = "Your OTP For Forgot Password Is"+str(otp)

            if address and subject and message:
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                    context['result'] = 'Email sent successfully'
                    request.session['email1']=request.POST['email']
                    request.session['otp']=otp
                except Exception as e:
                    context['result'] = f'Error sending email: {e}'
            else:
                context['result'] = 'All fields are required'
            
            return render(request, "otp.html", context)
        except:
            msg="Email Not Registered"
            return render(request,'forgot-password.html',{'msg':msg})

    else:
        return render(request,'forgot-password.html')


def verify_otp(request):
    if int(request.session['otp'])==int(request.POST['otp']):
        del request.session['otp']
        return render(request,'new-password.html')
    else:
        msg="Invalid OTP"
        return render(request, "otp.html",{'msg':msg})
    
def new_password(request):
    if request.POST['new_password']

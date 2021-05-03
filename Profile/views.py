from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Profile.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urlparams.redirect import param_redirect

# Create your views here.
def send_mail(reciever, name):
    MY_ADDRESS = "codecombatjuit@gmail.com"
    PASSWORD = "clashofcoders"

    print(reciever, name)

    s = smtplib.SMTP(host='smtp.gmail.com', port=587 or 465)
    s.starttls()

    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = '''Thank you for your participation.

Dear {name},

We the organizing team want to take a moment of your to thank you for the active participation of yours in our event Code Combat.


Your participation ensured the success of our event.

We hope you enjoyed and we look forward to seeing you at the next events as well.

Thank you for being at the event.


Team CODECOMBAT
while(!(succeed=try()));'''.format(name=name)

    msg['From']=MY_ADDRESS
    msg['To']=reciever
    msg['Subject'] = "Thank you for registering"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)

    del msg

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
        else :
            messages.error(request, "Invalid details.")
    return redirect('home')

def sign_up(request):
    if request.method == "POST":
        first_name = request.POST['f_name'].upper()
        last_name = request.POST['l_name'].upper()
        Phone = request.POST['phone']
        username = request.POST['username']
        Email = request.POST['email']
        College = request.POST['college']
        password = request.POST['password']
        
        user = authenticate(username=username, email=Email, password=password)
        
        if not user:
            new_user = User.objects.create_user(username=username, email=Email, password=password, first_name=first_name, last_name=last_name)
            new_user.save()
            
            new_profile = Profile.objects.create(User=new_user, Phone=Phone, College=College)            
            try:
                Image = request.FILES['image']
                new_profile.Image=Image
            except :
                pass
            new_profile.save()
            
            send_mail(new_profile.User.email, new_profile.User.first_name+" "+new_profile.User.last_name)
            
            login(request, new_user)
            messages.success(request, "You are now successfully registerd with us.")            
        else:
            res="user already exists."
            messages.error(request, res)    
    return redirect('home')

def sign_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
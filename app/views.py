from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def Home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'Home.html',d)
    return render(request,'Home.html')

def Registration(request):
    d={"UO":Userform(),"PO":ProfileForm()}
    if request.method=='POST' and request.FILES:
        USO=Userform(request.POST)
        PSO=ProfileForm(request.POST,request.FILES)
        if USO.is_valid() and PSO.is_valid():
            NUO=USO.save(commit=False)
            NUO.set_password(USO.cleaned_data['password'])
            NUO.save()
            NPO=PSO.save(commit=False)
            NPO.username=NUO
            NPO.save()
            send_mail('Registration',
                      "Registration is done successfully",
                      'kuruvakavita5@gmail.com',
                      [NUO.email],
                      fail_silently=False
                      )
            return HttpResponse("Data submitted Successfully!!!")
        else:
            return HttpResponse("OOPS Invalid Data Inserted!!!")
    return render(request,'Registration.html',d)

def User_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Home'))
        else:
            return HttpResponse("Invalid username or password!!!")

    return render(request,'User_login.html')

@login_required
def User_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))
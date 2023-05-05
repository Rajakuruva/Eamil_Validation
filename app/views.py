from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail
# Create your views here.

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
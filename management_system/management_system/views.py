from django.shortcuts import render,redirect
from django.http import HttpResponse


def Enter(request):
    
    html = render(request,"welcome.html")
    return HttpResponse(html)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def completed(request):
    return render(request, 'completed.html')

@login_required
def index(request):
    return redirect('news_main')

from django.shortcuts import render

def completed(request):
    return render(request, 'completed.html')

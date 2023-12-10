from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
    # Define more views for other pages

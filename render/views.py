from django.shortcuts import render

def index(request):
    return render(request, 'render/index.html', {})


def flight_profile(request):
    return render(request, 'flight_profile.html')


def drag_coefficient(request):
    return render(request, 'drag_coefficient.html')


def stability_time(request):
    return render(request, 'stability_time.html')


def motor_thrust_curve(request):
    return render(request, 'motor_thrust_curve.html')

from django.shortcuts import render

def index(request):
    return render(request, 'render/index.html', {})


def flight_profile(request):
    plot_image = None
    motor_name = ""

    if request.method == 'POST':
        motor_name = request.POST.get('motorName')

        # Process the motor name and generate the plot
        # For example, generate a plot and save it as an image or generate a plot URL

        plot_image = 'path_to_plot_image'  # Replace with actual plot path or URL

    # Render the same page with the form and plot (if available)
    return render(request, 'flight_profile.html', {'motor_name': motor_name, 'plot_image': plot_image})


def drag_coefficient(request):
    return render(request, 'drag_coefficient.html')


def stability_time(request):
    return render(request, 'stability_time.html')


def motor_thrust_curve(request):
    return render(request, 'motor_thrust_curve.html')

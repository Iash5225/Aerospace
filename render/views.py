from django.shortcuts import render
from .rocket import Rocket
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

def index(request):
    return render(request, 'render/index.html', {})


def plot_view(request):
    plot_image = None

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)

            # Process the file and generate plot
            rocket = Rocket(uploaded_file_url)
            rocket.set_motor_name("M2100")  # Set parameters as needed
            # ... other settings
            rocket.run()
            # Implement this method in Rocket class
            plot_image = rocket.get_plot_image_url()

    return render(request, 'yourapp/plot.html', {'plot_image': plot_image})


def flight_profile(request):
    plot_url = None
    motor_name = ""

    if request.method == 'POST':
        motor_name = request.POST.get('motorName')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            # fs = FileSystemStorage()
            # filename = fs.save(csv_file.name, csv_file)
            # # uploaded_file_url = fs.url(filename)
            # uploaded_file_path = fs.path(filename)  # Get the actual file path

            # Initialize Rocket class with the uploaded CSV file
            rocket = Rocket(csv_file.temporary_file_path())
            # rocket = Rocket(uploaded_file_path)
            rocket.set_motor_name(motor_name)
            rocket.set_PLOT_SAVE(True)

            # Generate the plot
            rocket.plot_Flight_Profile()  # Ensure this method saves the plot image

            # Get the URL or path of the saved plot image
            # plot_url = rocket.get_plot_image_url()  # Implement this method in Rocket class
            plot_url = rocket.plot_Flight_Profile()
            
            # Delete the temporary file
            # rocket.delete_temporary_file(plot_url)

    return render(request, 'flight_profile.html', {'plot_url': plot_url})



def drag_coefficient(request):
    return render(request, 'drag_coefficient.html')


def stability_time(request):
    return render(request, 'stability_time.html')


def motor_thrust_curve(request):
    return render(request, 'motor_thrust_curve.html')

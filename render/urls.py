from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# urlpatterns = [
#     path('', views.index, name='index'),
# ]

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('flight_profile/', views.flight_profile, name='flight_profile'),
    path('drag_coefficient/', views.drag_coefficient, name='drag_coefficient'),
    path('stability_time/', views.stability_time, name='stability_time'),
    path('motor_thrust_curve/', views.motor_thrust_curve,
         name='motor_thrust_curve'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This is only needed when running locally for development:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

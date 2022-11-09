from django.urls import path, include
from .import views
from .views import SignUpView


urlpatterns = [
    #path("updatedb/", views.update_location, name="updatedb"),
    path("updatedb/", views.update_database, name='updatedb'),
    path("signup/", SignUpView.as_view(), name="signup"),
]
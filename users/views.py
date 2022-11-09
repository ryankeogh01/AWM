from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# @login_required
# def update_location(request):
#     last_location = request.POST.get("point", None)
#
#     try:
#         user_profile = models.Profile.objects.get(user=request.user)
#         if not user_profile:
#             raise ValueError("Can't get User details")
#         point = request.POST["point"].split(",")
#         point = [float(part) for part in point]
#         point = Point(point, srid=4326)
#         user_profile.last_location = point(last_location)
#         user_profile.save()
#
#         return JsonResponse({"message": f"Set location to{point.wkt}."}, status=200)
#     except Exception as e:
#         return JsonResponse({"message": str(e)}, status=400)

@login_required
def update_database(request):
    """
    Updates the database with user location
    :param request:
    :return:
    """
    my_location = request.POST.get("point", None)
    if not my_location:
        return JsonResponse({"message": "No location found."}, status=400)

    try:
        my_coords = [float(coord) for coord in my_location.split(", ")]
        my_profile = request.user.profile
        my_profile.last_location = Point(my_coords)
        my_profile.save()

        message = f"Updated {request.user.username} with {f'POINT({my_location})'}"

        return JsonResponse({"message": message}, status=200)
    except:
        return JsonResponse({"message": "No profile found."}, status=400)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

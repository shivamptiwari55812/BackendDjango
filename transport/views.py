from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from app1.decorators import jwt_required
from .models import Transporter , Driver ,Driver_Location
# Create your views here.

@csrf_exempt
@jwt_required
def getDetails(request):
    if request.method =="POST":
        try:

            user=request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User not authenticated"}, status=401)
            print(request.body)
            data =json.loads(request.body)
            # if not request.user.is_authenticated:
            #  return JsonResponse({"message":"User not authenticated"},status=401)

            Transporter_obj = Transporter.objects.create(
                TransporterName = data.get("TransporterName",'None'),
                TransporterAddress = data.get("TransporterAddress"),
                Transporter_Contact = data.get("TransporterContact"),
                Transporter_Email = data.get("TransporterEmail"),
                user=user
            )
            Drivers_obj = Driver.objects.create(
                Driver_Name = data.get("DriverName"),
                Vehicle_Number = data.get("Vehicle_Number"),
                Driver_Contact = data.get("DriverContact"),
                Driver_Email = data.get("DriverEmail"),
                Transporter=Transporter_obj
            )

            return JsonResponse({"message":"Saved Successfully"},status=200)
        except Exception as e :
          import traceback
          traceback.print_exc()  
          return JsonResponse({"error": str(e)}, status=400)
        except:
            return JsonResponse({"message":"Not a valid Request"},status=400)
    
    return JsonResponse({"Invalid Error"},status=400)


# @csrf_exempt
# def Driverget(request):
#     if request.method == "POST":
#         try:
#             print(request.body)
#             data = json.loads(request.body)
#             # if not request.user.is_authenticated:
#             #   return JsonResponse({"message":"User not authenticated"},status=401)
 
#             Drivers_obj = Driver.objects.create(
#                 Driver_Name = data.get("DriverName"),
#                 Vehicle_Number = data.get("Vehicle_Number"),
#                 Driver_Contact = data.get("DriverContact"),
#                 Driver_Email = data.get("DriverEmail")
#             )
#             return JsonResponse({"message":"Saved Successfully"},status=200)
#         except Exception as e:
#             return JsonResponse({"message":"Invalid request"},status=400)
#     return JsonResponse({"message":"Invalid request"},status=400)
            

@csrf_exempt
def saveLocation(request):
    if request.method == 'POST':
     try:
         data = json.loads(request.body)
         print(data)

         driver_obj = Driver_Location.objects.create(
             latitude = data.get("latitude"),
             longitude = data.get("longitude"),
         )

         return JsonResponse({'Successfull data fetched'})

     except Exception as e:
         return JsonResponse({"message":"Invalid "})
    else:
        return JsonResponse({"Invalid request"})
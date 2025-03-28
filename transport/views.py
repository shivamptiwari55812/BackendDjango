from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Transporter
# Create your views here.

@csrf_exempt
def TransporterSet(request):
    if request.method =="POST":
        try:
            print(request.body)
            data =json.loads(request.body)
            Transporter_obj = Transporter.objects.create(
                TransporterName = data.get("TransporterName "),
                TransporterAddress = data.get("TransporterAddress"),
                Transporter_Contact = data.get("TransporterContact"),
                Transporter_Email = data.get("TransporterEmail")
            )

            return JsonResponse({"message":"Saved Successfully"},status=200)
        except Exception as e :
            return JsonResponse({"message":"Not a valid Request"},status=400)
    
    return JsonResponse({"Invalid Error"},status=400)


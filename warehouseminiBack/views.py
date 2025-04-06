from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from invoice.models import InvoiceBill 


@csrf_exempt
def signup(request):
    if request.method =="POST":
        try:
            print(request.body)
            data =json.loads(request.body)
            username = data.get("fullName","")
            email = data.get("email","")
            password = data.get("password","")

            if not username or not email or not password:
                return JsonResponse({"message":"Invalid Request"},status=400)
            
            if User.objects.filter(username=username).exists():
                messages.info("This username exists already")
                return JsonResponse({"message":"Username already exists"},status=400)
                
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"Email already exists"},status=400)

            user_obj = User.objects.create_user(
                username=username,
                email=email,
                password=password    
            )
        
            user_obj.save()
            messages.info("Account created Successfully")
            messages.success(request, "Logged in successfully!")
            message_list = [message.message for message in messages.get_messages(request)]
            return JsonResponse({"message":"Saved Successfully","message":message_list},status=200)
        except Exception as e :
            return JsonResponse({"message":"Not a valid Request"},status=400)
        





@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            username = data.get("username", "")
            password = data.get("password", "")

            if not username or not password:
                return JsonResponse({"message": "Missing required fields"}, status=400)

            # Find the user by email and authenticate
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                messages.info("Invalid username or password ")
                return JsonResponse({"message": "Invalid username or password"}, status=401)
  
            user_authenticated = authenticate(username=username, password=password)
            
            if user_authenticated is None:
                return JsonResponse({"message": "Invalid email or password"}, status=401)
           
            try:
                login(request, user_authenticated)
                message_list = [message.message for message in messages.get_messages(request)]
                return JsonResponse({"message": "Logged in successfully","message":message_list}, status=200)
            
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid HTTP method"}, status=405)

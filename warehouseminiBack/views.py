from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CreateUserForm
from outbound.utils.email_service import send_mail,EmailMessage
from django.conf import settings
from invoice.models import InvoiceBill 
from registration.views import generate_and_store_otp
from registration.models import OTP
import random
from .jwt_utils import decode_jwt
from app1.decorators import jwt_required
from .jwt_utils import generate_jwt



@csrf_exempt

def SignUpview(request):
    form = CreateUserForm()
    if request.method == "POST":
     try: 
        print(request.body)
        data =json.loads(request.body)
        form_data ={
            'username' : data.get("username",""),
            'email' : data.get("email",""),
            'password1': data.get("password1", ""),
           'password2': data.get("password2", ""),
        }
        form = CreateUserForm(form_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active =False
            user.save()

            otp_code =generate_and_store_otp(user)
            message = f"""Dear {form_data['username']},
                Welcome to TG Software! 
                Your account has initiated the sign Up,
                Verify it using the OTP :-{otp_code}
         Best regards,
        TG Corporation Team
                """
                
            send_mail(
                    subject="Welcome to TG Software",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[form_data['email']], 
                    fail_silently=False,
                )
            
            return JsonResponse({"message":"Saved Successfully",},status=200)
        else:
            print(form.errors)
            return JsonResponse({"message":"Invalid form request"},status=400)       
     
     except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"message":"Invalid request"},status=405)
    
@csrf_exempt
def loginView(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            form_data = {
               'username': data.get("username", ""),
              'password': data.get("password", ""),
            }
            user = authenticate(request,username=form_data['username'],password=form_data['password'])
            
            if user is None:
                print("Shivam ")
                return JsonResponse({"message": "Invalid username or password"}, status=401)
            else:
                OTP.objects.filter(user=user).delete()
                otp_code = generate_and_store_otp(user)
                
                message= f"""Dear {form_data['username']},




                                   Here is OTP for Login :-  {otp_code}





                             Best regards,
                             TG Corporation Team
                          """

                send_mail(
                subject="OTP Verification for Login",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
                )

                return JsonResponse({"message": "Otp sent successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
        except Exception as e:
          print("Error in loginView:", e)
          return JsonResponse({"message": str(e)}, status=400)

    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
        

@csrf_exempt
@jwt_required
def logoutView(request):
 if request.method == "POST":
    logout()
    return JsonResponse({"message": "Logout successfull"}, status=200)
 else:
    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt

def verify_otp(request):
    if request.method == "POST":
        try:
            print(request.body)
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")
            
            # Find user by email
            try:
                user = User.objects.get(email=email)
                otp_instance = OTP.objects.filter(user=user).latest('created_at')
                
                if otp_instance.code == otp and not otp_instance.is_expired():
                    user.is_active = True  # Activate user
                    user.save()
                    token = generate_jwt(user.id)
                    print(token)
                    return JsonResponse({"message": "Verification successful","token":token}, status=200)
                
                return JsonResponse({"message": "Invalid or expired OTP"}, status=400)
            
            except User.DoesNotExist:
                return JsonResponse({"message": "User not found"}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def verify_login_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            otp = data.get("otp")
            
            if username and otp:
              try:
                  user = User.objects.get(username=username)
                  if user is not None:
                      otp_obj = OTP.objects.filter(user=user).latest('created_at')
                      if otp_obj.code == otp and not otp_obj.is_expired():
                          token = generate_jwt(user.id)
                          print(token)
                          return JsonResponse({"message": "Verification login successful","token":token,"username":user.username}, status=200)
                      else:
                          return JsonResponse({"message": "Invalid or expired OTP"}, status=400)
                  else:
                      return JsonResponse({"message": "User not found"}, status=404)
              except OTP.DoesNotExist:
                  return JsonResponse({"message": "OTP not found"}, status=404)
            else:
                return JsonResponse({"message": "Invalid request"}, status=400)
        except json.JSONDecodeError:
         return JsonResponse({"message": "Invalid JSON format"}, status=400)
    else:
     return JsonResponse({"message": "Invalid request method"}, status=405)

                                                                     
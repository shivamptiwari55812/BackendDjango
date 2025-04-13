# decorators.py
from django.http import JsonResponse
from warehouseminiBack.jwt_utils import decode_jwt
from django.contrib.auth.models import User

def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"message": "Unauthorized"}, status=401)

        token = auth_header.split(" ")[1]
        user_id = decode_jwt(token)

        if not user_id:
            return JsonResponse({"message": "Invalid or expired token"}, status=401)

        try:
            request.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=404)

        return view_func(request, *args, **kwargs)
    return wrapper

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import *
from django.contrib.auth.hashers import make_password


@csrf_exempt
def register(request):
    if request.method == "POST":

        # Loading json data into a var
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Initializing variables
        DNI = data.get("DNI", None)
        Name = data.get('Nombre', None)
        Surname = data.get('Apellidos', None)
        NPhone = data.get('Telefono', None)
        Email = data.get('Email', None)
        Password1 = data.get('Contraseña1', None)
        Password2 = data.get('Contraseña2', None)

        # Checks void variables and type datas
        if not(DNI or Name or Surname or NPhone or Email or Password1 or Password2):
            return JsonResponse({'error': 'bad input parameter. Void parameter'}, status=400)
        elif not isinstance(DNI, str) or not isinstance(Name, str) or not isinstance(Surname, str) or not isinstance(NPhone, str) or not isinstance(Email, str) or not isinstance(Password1, str):
            return JsonResponse({'error': 'bad input parameter. Wrong data type'}, status=400)
        else:
            if Empleado.objects.filter(dni=DNI).exists():  # Check out if the user exists
                return JsonResponse({'error': 'Conflict. User already exists'}, status=409)
            else:
                if not isinstance(DNI, str) or len(DNI) != 9:  # DNI checks
                    return JsonResponse({'error': 'bad input parameter. Wrong DNI'}, status=400)
                elif len(NPhone) != 9:  # Phone number checks
                    return JsonResponse({'error': 'bad input parameter. Wrong phone number'}, status=400)
                elif Password2 != Password1:  # Passwords checks
                    return JsonResponse({'error': 'bad input parameter. Passwords are not equals'}, status=400)
                else:
                    # We hash the password to secure it
                    hashed_password = make_password(Password1)

                    Empleado.objects.create(
                        dni=DNI,
                        nombre=Name,
                        apellidos=Surname,
                        telefono=NPhone,
                        email=Email,
                        contrasenha=hashed_password)
                    return JsonResponse({'message': 'employee created'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import *

# Password hashing dependences
from django.contrib.auth.hashers import make_password,check_password

# Token dependences
import jwt
import datetime


# GLOBAL VARIABLES
SECRET_KEY = "SecRetKeyDAW24"

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


def generate_token(dni):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), # Token expira en 1 día
        'iat': datetime.datetime.utcnow(),
        'id': dni
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


@csrf_exempt
def verify_token(request):

    # Initializing token
    token = request.META.get('HTTP_AUTHORIZATION', None)

    if not token:
        return JsonResponse({"Message": "Missing token"}, status=401), None
    else:
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]

            # Decoding token. This check out if it is expired or invalid
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return None, token
        except jwt.ExpiredSignatureError:
            return JsonResponse({"Error": "Token has expired"}, status=401), None
        except jwt.InvalidTokenError:
            return JsonResponse({"Error": "Token inválido"}, status=401), None


@csrf_exempt
def sign_in(request):
    if request.method == "POST":

        # Loading json data into a var
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Initializing variables
        dni = data.get('dni', None)
        password = data.get('password', None)

        if not(dni or password):
            return JsonResponse({'error': 'bad input parameter. Void parameter'}, status=400)
        else:
            # Check out parameters: data type, lenght, BD...
            if not isinstance(dni, str) or not isinstance(password, str):
                return JsonResponse({'error': 'bad input parameter. Wrong data type'}, status=400)
            elif len(dni) != 9:
                return JsonResponse({'error': 'bad input parameter. Wrong DNI'}, status=400)
            elif not Empleado.objects.filter(dni=dni).exists():
                return JsonResponse({'error': 'The user does not exists'}, status=404)
            else:
                # Check out if the passwords are equals
                BDpassword = Empleado.objects.get(dni=dni).contrasenha

                if check_password(password, BDpassword):
                    # Generate the token, save it and return it
                    token = generate_token(dni)

                    Empleado.objects.filter(dni=dni).update(token=token)
                    return JsonResponse({
                        'message': 'Log in successfully',
                        'token': token
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Wrong password!'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def sign_out(request):
    if request.method == "POST":
        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        # Check out if the session exists
        if Empleado.objects.filter(token=token).exists():

            # Delete session token from BD
            Empleado.objects.filter(token=token).update(token=None)
            return JsonResponse({'message': 'Signed out successfully !'}, status=200)
        else:
            return JsonResponse({'error': 'No session with that token !!'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def holidaysNabsences(request):
    if request.method == "GET":

        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        if Empleado.objects.filter(token=token).exists():

            # Take DNI and make the query
            dni = Empleado.objects.get(token=token).dni

            if VacacionesAusencias.objects.filter(empleado=dni).exists():
                query = VacacionesAusencias.objects.filter(empleado=dni)

                # Array to append data rows
                holiday_absencesArray = []
                for row in query:
                    # Json with each data row
                    json_data = {
                        'id': row.id,
                        'subject': row.asunto,
                        'type': row.tipo,
                        'start_date': row.fecha_inicio,
                        'finish_date': row.fecha_fin,
                        'comments': row.comentario
                    }

                    holiday_absencesArray.append(json_data)

                return JsonResponse({'data': holiday_absencesArray})
            else:
                return JsonResponse({'data': 'No data for this employee'})
        else:
            return JsonResponse({'error': 'No session with that token !!'})





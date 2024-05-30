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

# Paginator
from django.core.paginator import Paginator


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

                return JsonResponse({'data': holiday_absencesArray}, status=200)
            else:
                return JsonResponse({'data': 'No data for this employee'}, status=200)
        else:
            return JsonResponse({'error': 'No session with that token !!'}, status=404)

    elif request.method == "POST":

        # Loading json data into a var
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Initializing variables
        subject = data.get("Asunto", None)
        type = data.get("Tipo", None)
        start_date = data.get("Fecha inicio", None)
        finish_date = data.get("Fecha fin", None)
        comments = data.get("Comentarios", None)

        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        if Empleado.objects.filter(token=token).exists():

            # Take Empleado primary key
            employee = Empleado.objects.get(token=token)

            if not(subject or type or start_date or finish_date):
                return JsonResponse({'error': 'Bad input parameter. Void variable'}, status=400)
            elif not isinstance(subject, str) or not isinstance(type, str):
                return JsonResponse({'error': 'Wrong data'})
            elif subject == "" or type == "" or start_date == "" or finish_date == "":
                return JsonResponse({'error': 'Bad input parameter. Void variable'}, status=400)
            else:  # Validate dates
                try:
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                    finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return JsonResponse({'error': 'Invalid date format. Expected YYYY-MM-DD.'}, status=400)

                # New register
                VacacionesAusencias.objects.create(
                    asunto=subject,
                    tipo=type,
                    fecha_inicio=start_date,
                    fecha_fin=finish_date,
                    comentario=comments,
                    empleado=employee)
                return JsonResponse({'message': 'Register created !'})
        else:
            return JsonResponse({'error': 'No session with that token !!'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed '}, status=405)


@csrf_exempt
def notifications(request):
    if request.method == "GET":

        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        if Empleado.objects.filter(token=token).exists():

            # Take DNI and make the query
            dni = Empleado.objects.get(token=token).dni

            if Notificaciones.objects.filter(receptor=dni).exists():
                query = Notificaciones.objects.filter(receptor=dni)

                # Array to append data rows
                notificationsArray = []
                for row in query:
                    # Json with each data row
                    json_data = {
                        'id': row.id,
                        'subject': row.asunto,
                        'date': row.fecha,
                        'hour': row.hora,
                        'text': row.texto,
                        'sender': {
                            'name': row.emisor.nombre,
                            'surname': row.emisor.apellidos
                        }
                    }

                    notificationsArray.append(json_data)

                return JsonResponse({'data': notificationsArray}, status=200)
            else:
                return JsonResponse({'data': 'No data for this employee'})
        else:
            return JsonResponse({'error': 'No session with that token !!'})

    elif request.method == "POST":

        # Loading json data into a var
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Initializing variables
        receiver = data.get("Destinatario", None)
        subject = data.get("Asunto", None)
        date = data.get("Fecha", None)
        hour = data.get("Hora", None)
        text = data.get("Texto", None)

        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        if Empleado.objects.filter(token=token).exists():

            # Take Empleado primary key
            employee = Empleado.objects.get(token=token)

            if Empleado.objects.filter(dni=receiver).exists():

                receiver = Empleado.objects.get(dni=receiver)

                if not(subject or date or hour or text or receiver):
                    return JsonResponse({'error': 'Bad input parameter. Void variable'}, status=400)
                elif not isinstance(subject, str) or not isinstance(date, str) or not isinstance(hour, str) or not isinstance(text, str):
                    return JsonResponse({'error': 'Wrong data'})
                elif subject == "" or date == "" or hour == "" or text == "" or receiver == "":
                    return JsonResponse({'error': 'Bad input parameter. Void variable'}, status=400)
                else:  # Validate dates
                    try:
                        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                        hour = datetime.datetime.strptime(hour, '%H:%M')
                    except (ValueError, TypeError):
                        return JsonResponse({'error': 'Invalid date format. Expected YYYY-MM-DD.'}, status=400)

                    # New register
                    Notificaciones.objects.create(
                        asunto=subject,
                        fecha=date,
                        hora=hour,
                        texto=text,
                        emisor=employee,
                        receptor=receiver)
                    return JsonResponse({'message': 'Notifications sent !'})
            else:
                return JsonResponse({'error': 'No user with that DNI'}, status=409)
        else:
            return JsonResponse({'error': 'No session with that token !!'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed '}, status=405)


@csrf_exempt
def lastAccess(request):
    if request.method == "GET":

        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        if Empleado.objects.filter(token=token).exists():

            # Take DNI and make the query
            dni = Empleado.objects.get(token=token).dni

            if Registros.objects.filter(empleado=dni).exists():

                # Take the last access
                query = Registros.objects.filter(empleado=dni).order_by('-fecha', '-hora').first()

                json_data = {
                    'date': query.fecha,
                    'time': query.hora,
                    'type': query.tipo
                }

                return JsonResponse({'data': json_data}, status=200)
            else:
                return JsonResponse({'message': 'No data for this employee !!'}, status=200)
        else:
            return JsonResponse({'error': 'No session with that token !!'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed !'}, status=405)


@csrf_exempt
def trackday_log(request):
    if request.method == "GET":

        # Verifing token
        error_token, token = verify_token(request)

        if error_token:
            return error_token

        if Empleado.objects.filter(token=token).exists():

            # Take DNI and make the query
            dni = Empleado.objects.get(token=token).dni

            if Registros.objects.filter(empleado=dni).exists():

                # Make query
                query = Registros.objects.filter(empleado=dni)

                # Paging
                paginator = Paginator(query, 10)  # By default, it is limited to 10 registries
                page = request.GET.get("page", 1)
                registries = paginator.get_page(page)
                trackdayArray = []

                for registrie in registries:
                    trackdayArray.append({
                         "type": registrie.tipo,
                         "hour": registrie.hora,
                         "date": registrie.fecha,
                         "comments": registrie.comentarios
                    })

                json_data = {
                    'trackdays': trackdayArray,
                    'page': page
                }

                return JsonResponse({'data': json_data}, status=200)
            else:
                return JsonResponse({'message': 'No data for this employee !!'}, status=200)
        else:
            return JsonResponse({'error': 'No session with that token !!'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed !'}, status=405)


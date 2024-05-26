# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empleado(models.Model):
    dni = models.CharField(db_column='DNI', primary_key=True, max_length=9)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(db_column='Apellidos', max_length=70)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    contrasenha = models.CharField(db_column='Contrasenha', max_length=100)  # Field name made lowercase.
    token = models.CharField(db_column='Token', max_length=200, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'empleado'


class Notificaciones(models.Model):
    asunto = models.CharField(db_column='Asunto', max_length=100)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    hora = models.TimeField(db_column='Hora')  # Field name made lowercase.
    texto = models.CharField(db_column='Texto', max_length=500)  # Field name made lowercase.
    emisor = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='Emisor', related_name='emisor')  # Field name made lowercase.
    receptor = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='Receptor', related_name='receptor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'notificaciones'


class Registros(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=13)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha')  # Field name made lowercase.
    hora = models.TimeField(db_column='Hora')  # Field name made lowercase.
    comentarios = models.CharField(db_column='Comentarios', max_length=300, blank=True, null=True)  # Field name made lowercase.
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='Empleado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registros'


class Tareas(models.Model):
    titulo = models.CharField(db_column='Titulo', max_length=100)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=1000)  # Field name made lowercase.
    fecha_asignacion = models.DateField(db_column='Fecha_asignacion')  # Field name made lowercase.
    fecha_vencimiento = models.DateField(db_column='Fecha_vencimiento')  # Field name made lowercase.
    prioridad = models.CharField(db_column='Prioridad', max_length=5, blank=True, null=True)  # Field name made lowercase.
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='Empleado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tareas'


class VacacionesAusencias(models.Model):
    asunto = models.CharField(db_column='Asunto', max_length=100)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fecha_inicio = models.DateField(db_column='Fecha_inicio')  # Field name made lowercase.
    fecha_fin = models.DateField(db_column='Fecha_fin')  # Field name made lowercase.
    comentario = models.CharField(db_column='Comentario', max_length=1000)  # Field name made lowercase.
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='Empleado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vacaciones_ausencias'

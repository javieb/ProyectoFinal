create database MiEmpleado;
use MiEmpleado;

create table empleado(
	DNI char(9) PRIMARY KEY,
    Nombre varchar(50) not null,
    Apellidos varchar(70) not null,
    Email varchar(50) not null,
    Contrasenha varchar(100) not null,
    Token varchar(200),
    Telefono varchar(20)
);

create table registros(
	id integer auto_increment PRIMARY KEY,
    Tipo enum("Salida", "Entrada", "Entrada-pausa", "Salida-pausa") not null,
    Fecha date not null,
    Hora time not null,
    Comentarios varchar(300),
    Empleado char(9) not null
);

create table tareas(
	id integer auto_increment PRIMARY KEY,
    Titulo varchar(100) not null,
    Descripcion varchar(1000) not null,
    Fecha_asignacion date not null,
    Fecha_vencimiento date not null,
    Prioridad enum("Baja", "Media", "Alta"),
    Empleado char(9) not null
);

create table notificaciones(
	id integer auto_increment PRIMARY KEY,
    Asunto varchar(100) not null,
    Fecha date not null,
    Hora time not null,
    Texto varchar(500) not null,
    Emisor char(9) not null,
    Receptor char(9) not null
);

create table vacaciones_ausencias(
	id integer auto_increment PRIMARY KEY,
    Asunto varchar(100) not null,
    Tipo enum("Vacaciones", "Ausencia"),
    Fecha_inicio date not null,
    Fecha_fin date not null,
    Comentario varchar(1000) not null,
    Empleado char(9) not null
);

/*INSERCIONES*/
-- Insertar empleado 
INSERT INTO empleado (DNI, Nombre, Apellidos, Email, Contrasenha, Token, Telefono) 
VALUES ('123456789', 'Juan', 'Pérez Gómez', 'juan@example.com', 'contrasenha123', NULL, '123456789');
INSERT INTO empleado (DNI, Nombre, Apellidos, Email, Contrasenha, Token, Telefono) 
VALUES ('012345678', 'Pepe', 'Pérez Gómez', 'pepe@example.com', 'contrasenha123', NULL, '123456789');

-- Insertar un registro
INSERT INTO registros (Tipo, Fecha, Hora, Comentarios, Empleado)
VALUES ('Entrada', '2024-05-04', '08:00:00', 'Inicio de jornada laboral', '123456789');

-- Insertar una tarea
INSERT INTO tareas (Titulo, Descripcion, Fecha_asignacion, Fecha_vencimiento, Prioridad, Empleado)
VALUES ('Revisar informe mensual', 'Revisar el informe de ventas del mes pasado y preparar un resumen ejecutivo.', '2024-05-04', '2024-05-10', 'Alta', '123456789');

-- Insertar una notificación
INSERT INTO notificaciones (Asunto, Fecha, Hora, Texto, Emisor, Receptor)
VALUES ('Recordatorio de reunión', '2024-05-04', '09:00:00', 'Recordatorio de la reunión de equipo a las 10:00 AM.', '123456789', '012345678');

-- Insertar una solicitud de vacaciones
INSERT INTO vacaciones_ausencias (Asunto, Tipo, Fecha_inicio, Fecha_fin, Comentario, Empleado)
VALUES ('Vacaciones de verano', 'Vacaciones', '2024-07-01', '2024-07-15', 'Vacaciones anuales planificadas', '123456789');


/*FOREIGN KEYS*/

alter table registros add constraint fk_registro_empleado foreign key (Empleado) references empleado(DNI) on delete cascade on update cascade;
alter table tareas add constraint fk_tareas_empleado foreign key (Empleado) references empleado(DNI) on delete cascade on update cascade;
alter table notificaciones add constraint fk_notificaciones_sender_empleado foreign key (Emisor) references empleado(DNI) on delete cascade on update cascade;
alter table notificaciones add constraint fk_notificacines_receiver_empleado foreign key (Receptor) references empleado(DNI) on delete cascade on update cascade;
alter table vacaciones_ausencias add constraint fk_vacaciones_ausencias_empleado foreign key (Empleado) references empleado(DNI) on delete cascade on update cascade;








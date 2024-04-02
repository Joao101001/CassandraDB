CREATE KEYSPACE bdtest
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE bdtest.students (
    student_id UUID PRIMARY KEY,
    student_name TEXT,
    student_carnet_id TEXT
);

CREATE TABLE bdtest.teachers (
    teacher_id UUID PRIMARY KEY,
    teacher_name TEXT,
    teacher_carnet_id TEXT
);

CREATE TABLE bdtest.employees (
    employee_id UUID PRIMARY KEY,
    employee_name TEXT,
    employee_carnet_id TEXT
);

CREATE TABLE bdtest.access_logs (
    access_id UUID,
    person_id UUID,
    person_type TEXT,
    person_name TEXT,
    access_time TIMESTAMP,
    access_type TEXT,
    location TEXT,
    PRIMARY KEY ((access_time), access_id)
) WITH CLUSTERING ORDER BY (access_id DESC);


CREATE TABLE bdtest.classrooms (
    classroom_id UUID PRIMARY KEY,
    classroom_name TEXT
);

CREATE TABLE bdtest.halls (
    hall_id UUID PRIMARY KEY,
    hall_name TEXT
);

CREATE TABLE bdtest.person_classroom (
    person_id UUID,
    classroom_id UUID,
    PRIMARY KEY (person_id, classroom_id)
);

CREATE TABLE bdtest.person_hall (
    person_id UUID,
    hall_id UUID,
    PRIMARY KEY (person_id, hall_id)
);


INSERT INTO bdtest.employees (employee_id, employee_name, employee_carnet_id) VALUES (uuid(), 'Empleado 1', 'carnet_empleado_1');
INSERT INTO bdtest.teachers (teacher_id, teacher_name, teacher_carnet_id) VALUES (uuid(), 'Maestro 1', 'carnet_maestro_1');
INSERT INTO bdtest.students (student_id, student_name, student_carnet_id) VALUES (uuid(), 'Estudiante 1', 'carnet_estudiante_1');

select * from students;
select * from teachers;
select * from employees;

select * from access_logs                   ;

truncate table access_logs;

CREATE INDEX ON bdtest.access_logs (access_id);



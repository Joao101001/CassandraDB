from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4, UUID
from datetime import datetime
import random
import time
from concurrent.futures import ThreadPoolExecutor
import threading


auth_provider = PlainTextAuthProvider(username='cassandra', password='')
cluster = Cluster(['localhost'], auth_provider=auth_provider)
session = cluster.connect('bdtest')


locations = ["Aula 101", "Aula 202", "Salón Principal", "Biblioteca", "Laboratorio"]


people = [
    {"type": "estudiante", "id": "3adbb0fe-9778-4354-8b2a-fe43511ddf38", "name": "Estudiante 1"},
    {"type": "maestro", "id": "48894184-2b66-45ce-9c83-3a3fa566fe93", "name": "Maestro 1"},
    {"type": "empleado", "id": "239f61a6-1105-4c39-aca4-2499e03e1152", "name": "Empleado 1"}
]

# Función para insertar un registro de acceso
def insert_access_log(person_id, person_type, person_name, access_type, location):
    access_id = uuid4()
    access_time = datetime.now()
    person_id = UUID(person_id)


    query = "INSERT INTO access_logs (access_id, person_id, person_type, person_name, access_time, access_type, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"


    session.execute(query, (access_id, person_id, person_type, person_name, access_time, access_type, location))


    result = session.execute("SELECT * FROM access_logs WHERE access_id = %s", (access_id,))
    if result:
        print(f"Registro de acceso insertado correctamente para {person_type} {person_id}")
    else:
        print(f"Error al insertar registro de acceso para {person_type} {person_id}")


    print(
        f"Tipo de acceso: {access_type}, ubicación: {location}, tiempo de acceso: {access_time}")


def modify_data_concurrently():
    print("\nIntentando modificar datos mientras se insertan...")


    person = random.choice(people)
    person_id = person["id"]
    person_type = person["type"]
    person_name = person["name"]
    access_type = random.choice(["entrada", "salida"])
    location = random.choice(locations)


    for _ in range(10):

        insert_access_log(person_id, person_type, person_name, access_type, location)
        time.sleep(0.1)
def simulate_accesses_and_optimization_tests(num_accesses):
    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        for _ in range(num_accesses):
            executor.submit(modify_data_concurrently)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nSe han simulado {num_accesses} accesos en {execution_time:.2f} segundos")


def stress_test_database(num_threads, num_operations_per_thread):
    print("\nPrueba de estrés en la base de datos:")


    threads = []


    def stress_thread():
        for _ in range(num_operations_per_thread):

            person = random.choice(people)
            person_id = person["id"]
            person_type = person["type"]
            person_name = person["name"]
            access_type = random.choice(["entrada", "salida"])
            location = random.choice(locations)


            insert_access_log(person_id, person_type, person_name, access_type, location)


    for _ in range(num_threads):
        thread = threading.Thread(target=stress_thread)
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    print(f"Prueba de estrés completada con {num_threads} hilos y {num_operations_per_thread} operaciones por hilo.")


def test_data_security():
    print("\nPrueba de seguridad de datos:")

    query = "SELECT * FROM access_logs"
    result = session.execute(query)

    # Verificar si hay registros
    if result:
        print("¡Los datos están seguros!")
    else:
        print("¡Error! Los datos no están seguros.")


if __name__ == "__main__":
    num_accesses = 100
    num_threads = 10
    num_operations_per_thread = 10

    simulate_accesses_and_optimization_tests(num_accesses)
    test_data_security()
    stress_test_database(num_threads, num_operations_per_thread)

# Cerrar la conexión a Cassandra al finalizar
session.shutdown()
cluster.shutdown()
